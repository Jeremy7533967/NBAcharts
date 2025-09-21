"""
爬蟲 DAG
爬取數據，並上傳至 MySQL 資料庫
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from data_ingestion.nba_news_headline import nba_news_headline
from data_ingestion.nba_news_udn import nba_news_udn



#%% function
# 包裝函數，避免序列化問題: """觸發爬蟲任務"""
def trigger_nba_news_headline():
    nba_news_headline()

def trigger_nba_news_udn():
    nba_news_udn()


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
    dag_id='crawler_NBA_news',
    default_args=default_args,
    description='nba news headline',
    schedule_interval='0 9 * * *',  # 每天早上 9 點執行
    catchup=False,  # 不執行歷史任務
    max_active_runs=1,  # 同時只允許一個 DAG 實例運行
    tags=['NBA', 'crawler', 'news', 'headline'],
) as dag:

    ### 開始任務
    start_task = BashOperator(
        task_id='start_crawler',
        bash_command='echo "開始"',
    )

    # # NBA news headline
    nba_news1 = PythonOperator(
        task_id=f'nba_news_headline',
        python_callable=trigger_nba_news_headline,
    )
    # NBA news udn
    nba_news2 = PythonOperator(
        task_id=f'nba_news_udn',
        python_callable=trigger_nba_news_udn,
    )


    ### 結束任務
    end_task = BashOperator(
        task_id='end_crawler',
        bash_command='echo "結束"',
        trigger_rule='all_success',  # 只有當所有前置任務成功時才執行
    )

    # 設定任務依賴關係
    # 開始 -> 環境驗證 -> 兩個分流 -> 各自的爬取任務 -> 結束
    start_task >> [nba_news1,nba_news2] >> end_task
