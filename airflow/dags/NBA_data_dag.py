"""
爬蟲 DAG
爬取數據，並上傳至 MySQL 資料庫
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from data_ingestion.nba_players_salary import player_year_salary
from data_ingestion.nba_players_state import nba_players_state
from data_ingestion.nba_teams_salary import nba_teams_salary
from data_ingestion.nba_teams_state import nba_teams_state
from data_ingestion.nba_teams_advance import nba_teams_advancedstate
from data_ingestion.dataprocess import team_data_merge
from data_ingestion.dataprocess import player_data_merge


#%% 定義要爬取的年份
years_1 = list(range(2015,2026))
years_2 = list(range(2014,2025))


#%% function
# 包裝函數，避免序列化問題: """觸發爬蟲任務"""
def trigger_player_salary_crawler(year):
    player_year_salary(year)

def trigger_player_state_crawler(year):
    nba_players_state(year)

def trigger_team_salary_crawler(year):
    nba_teams_salary(year)

def trigger_team_state_crawler(year):
    nba_teams_state(year)

def trigger_team_advance_crawler(year):
    nba_teams_advancedstate(year)

def trigger_team_merge():
    team_data_merge()

def trigger_player_merge():
    player_data_merge()

#%% GAD definition
# 預設參數
default_args = {
    'owner': 'data-team',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,  # 失敗時重試次數
    'retry_delay': timedelta(minutes=1),  # 重試間隔分鐘
    'execution_timeout': timedelta(hours=1),  # 執行超時時間 1 小時
}


# 建立 DAG
with DAG(
    dag_id='crawler_NBA_data',
    default_args=default_args,
    description='nba player & team information',
    schedule_interval=None,  
    catchup=False,  # 不執行歷史任務
    max_active_runs=1,  # 同時只允許一個 DAG 實例運行
    tags=['NBA', 'crawler', 'player', 'team'],
) as dag:

    ### 開始任務
    start_task = BashOperator(
        task_id='start_crawler',
        bash_command='echo "開始執行爬蟲任務..."',
    )

    ### 分流 dummy task
    # player
    player_branch = DummyOperator(
        task_id='player_branch',
    )

    # team
    team_branch = DummyOperator(
        task_id='team_branch',
    )


    ### crawler
    # player salary
    player_salary_tasks = []
    for year in years_2:
        player_salary_tasks.append(
            PythonOperator(
            task_id=f'{year+1}_player_salary',
            python_callable=trigger_player_salary_crawler,
            op_args=[year],
        ))

    # player state
    task_player_state = PythonOperator(
        task_id=f'player_state',
        python_callable=trigger_player_state_crawler,
        op_args=[years_1],
    )

    # player merge
    player_merge = PythonOperator(
        task_id=f'player_merge',
        python_callable=trigger_player_merge,
    )

    # team salary
    task_team_salary = PythonOperator(
        task_id=f'team_salary',
        python_callable=trigger_team_salary_crawler,
        op_args=[years_2],
    )


    # team state
    task_team_state = PythonOperator(
        task_id=f'team_state',
        python_callable=trigger_team_state_crawler,
        op_args=[years_1],
    )


    # team state
    task_team_advance = PythonOperator(
        task_id=f'team_advance',
        python_callable=trigger_team_advance_crawler,
        op_args=[years_1],
    )

    # team merge
    team_merge = PythonOperator(
        task_id=f'team_merge',
        python_callable=trigger_team_merge,
    )


    ### 結束任務
    end_task = BashOperator(
        task_id='end_crawler',
        bash_command='echo "爬蟲任務發送完成！"',
        trigger_rule='all_success',  # 只有當所有前置任務成功時才執行
    )

    # 設定任務依賴關係
    # 開始 -> 環境驗證 -> 兩個分流 -> 各自的爬取任務 -> 結束
    start_task >> player_branch >> task_player_state >> player_merge >> end_task
    start_task >> player_branch >> player_salary_tasks >> player_merge >> end_task
    start_task >> team_branch >> [task_team_salary,task_team_advance,task_team_state] >> team_merge >> end_task
