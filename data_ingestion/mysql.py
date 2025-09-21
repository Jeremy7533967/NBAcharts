import pandas as pd
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）
from sqlalchemy import Column, Float, MetaData, String, Table, Integer, Text, DECIMAL, DATETIME, PrimaryKeyConstraint, ForeignKey, Date
from sqlalchemy.dialects.mysql import insert

from data_ingestion.config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT

MYSQL_DATABASE = "NBA"

# 創建元資料
metadata = MetaData()

# player salsry
nba_player_salary_table = Table(
    "nba_player_salary",  # 資料表名稱
    metadata,
    Column("year", Integer, nullable=False, comment="年度"),
    Column("player", String(100),nullable=False, comment="球員名稱"),
    Column("team", String(50), nullable=False, comment="球隊名稱"),
    Column("salary", Integer, nullable=True, comment="薪水"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間"),
    PrimaryKeyConstraint("year", "player", "team")
)

# player state
nba_player_state_table = Table(
    "nba_player_state",  # 資料表名稱
    metadata,
    Column("year", Integer, nullable=False, comment="年度"),
    Column("player", String(100), nullable=False, comment="球員名稱"),	
    Column("team", String(50), nullable=False, comment="球隊名稱"),
    Column("age", Integer, nullable=True, comment="年齡"),
    Column("pos", String(50), nullable=True, comment="位置"),	
    Column("games", Integer, nullable=True, comment="參與比賽數"),	
    Column("games_started", Integer, nullable=True, comment="先發次數"),	
    Column("minutes_played", Integer, nullable=True, comment="總上場時間"),	
    Column("field_goals", Integer, nullable=True, comment="投籃命中數"),
    Column("field_goals_attempts", Integer, nullable=True, comment="投籃次數"),	
    Column("field_goals_percentage", Float, nullable=True, comment="投籃命中率"),	
    Column("3p_field_goals", Integer, nullable=True, comment="三分球命中數"),	
    Column("3p_field_goals_attempts", Integer, nullable=True, comment="三分球出手次數"),	
    Column("3p_field_goals_percentage", Float, nullable=True, comment="三分球命中率"),
    Column("2p_field_goals", Integer, nullable=True, comment="兩分球命中數"),	
    Column("2p_field_goals_attempts", Integer, nullable=True, comment="兩分球出手次數"),	
    Column("2p_field_goals_percentage", Float, nullable=True, comment="兩分球命中率"),	
    Column("efg_pct", Float, nullable=True, comment="有效投籃命中率_增加三分球價值"),
    Column("free_throws", Integer, nullable=True, comment="罰球命中數"),	
    Column("free_throws_attempts", Integer, nullable=True, comment="罰球出手次數"),	
    Column("free_throws_percentage", Float, nullable=True, comment="罰球命中率"),	
    Column("offensive_rebounds", Integer, nullable=True, comment="進攻籃板數"),	
    Column("defensive_rebounds", Integer, nullable=True, comment="防守籃板數"),	
    Column("total_rebounds", Integer, nullable=True, comment="總籃板數"),	
    Column("assists", Integer, nullable=True, comment="助攻數"),
    Column("steals", Integer, nullable=True, comment="抄截數"),	
    Column("blocks", Integer, nullable=True, comment="阻攻數"),	
    Column("turnovers", Integer, nullable=True, comment="失誤數"),	
    Column("personal_fouls", Integer, nullable=True, comment="犯規數"),	
    Column("points", Integer, nullable=True, comment="得分"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間"),
    PrimaryKeyConstraint("year", "player", "team")
)

# player merge
nba_player_table = Table(
    "nba_player_table",  # 資料表名稱
    metadata,
    Column("year", Integer, nullable=False, comment="年度"),
    Column("player", String(100),nullable=False, comment="球員名稱"),
    Column("team", String(50), nullable=False, comment="球隊名稱"),
    Column("salary", Integer, nullable=True, comment="薪水"),
    Column("age", Integer, nullable=True, comment="年齡"),
    Column("pos", String(50), nullable=True, comment="位置"),	
    Column("games", Integer, nullable=True, comment="參與比賽數"),	
    Column("games_started", Integer, nullable=True, comment="先發次數"),	
    Column("minutes_played", Integer, nullable=True, comment="總上場時間"),	
    Column("field_goals", Integer, nullable=True, comment="投籃命中數"),
    Column("field_goals_attempts", Integer, nullable=True, comment="投籃次數"),	
    Column("field_goals_percentage", Float, nullable=True, comment="投籃命中率"),	
    Column("3p_field_goals", Integer, nullable=True, comment="三分球命中數"),	
    Column("3p_field_goals_attempts", Integer, nullable=True, comment="三分球出手次數"),	
    Column("3p_field_goals_percentage", Float, nullable=True, comment="三分球命中率"),
    Column("2p_field_goals", Integer, nullable=True, comment="兩分球命中數"),	
    Column("2p_field_goals_attempts", Integer, nullable=True, comment="兩分球出手次數"),	
    Column("2p_field_goals_percentage", Float, nullable=True, comment="兩分球命中率"),	
    Column("efg_pct", Float, nullable=True, comment="有效投籃命中率_增加三分球價值"),
    Column("free_throws", Integer, nullable=True, comment="罰球命中數"),	
    Column("free_throws_attempts", Integer, nullable=True, comment="罰球出手次數"),	
    Column("free_throws_percentage", Float, nullable=True, comment="罰球命中率"),	
    Column("offensive_rebounds", Integer, nullable=True, comment="進攻籃板數"),	
    Column("defensive_rebounds", Integer, nullable=True, comment="防守籃板數"),	
    Column("total_rebounds", Integer, nullable=True, comment="總籃板數"),	
    Column("assists", Integer, nullable=True, comment="助攻數"),
    Column("steals", Integer, nullable=True, comment="抄截數"),	
    Column("blocks", Integer, nullable=True, comment="阻攻數"),	
    Column("turnovers", Integer, nullable=True, comment="失誤數"),	
    Column("personal_fouls", Integer, nullable=True, comment="犯規數"),	
    Column("points", Integer, nullable=True, comment="得分"),
    PrimaryKeyConstraint("year", "player", "team")
)

# team salary
nba_team_salary_table = Table(
    "nba_team_salary",  # 資料表名稱
    metadata,
    Column("year",Integer,primary_key=True,comment="年度"),
    Column("team",String(50),primary_key=True,comment="球隊名稱"),
    Column("salary",Integer,nullable=True,comment="球隊總薪資"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間")
)

# team state
nba_team_state_table = Table(
    "nba_team_state",  # 資料表名稱
    metadata,
    Column("year",Integer,primary_key=True,comment="年度"),
    Column("team",String(50),primary_key=True,comment="球隊名稱"),
    Column("games",Integer,nullable=True,comment="參與比賽數"),
    Column("minutes_played",Integer,nullable=True,comment="總上場時間"),
    Column("field_goals",Integer,nullable=True,comment="投籃命中數"),
    Column("field_goals_attempts",Integer,nullable=True,comment="投籃次數"),
    Column("field_goals_percentage",Float,nullable=True,comment="投籃命中率"),
    Column("3p_field_goals",Integer,nullable=True,comment="三分球命中數"),
    Column("3p_field_goals_attempts",Integer,nullable=True,comment="三分球出手次數"),
    Column("3p_field_goals_percentage",Float,nullable=True,comment="三分球命中率"),
    Column("2p_field_goals",Integer,nullable=True,comment="兩分球命中數"),
    Column("2p_field_goals_attempts",Integer,nullable=True,comment="兩分球出手次數"),
    Column("2p_field_goals_percentage",Float,nullable=True,comment="兩分球命中率"),
    Column("free_throws",Integer,nullable=True,comment="罰球命中數"),
    Column("free_throws_attempts",Integer,nullable=True,comment="罰球出手次數"),
    Column("free_throws_percentage",Float,nullable=True,comment="罰球命中率"),
    Column("offensive_rebounds",Integer,nullable=True,comment="進攻籃板數"),
    Column("defensive_rebounds",Integer,nullable=True,comment="防守籃板數"),
    Column("total_rebounds",Integer,nullable=True,comment="總籃板數"),
    Column("assists",Integer,nullable=True,comment="助攻數"),
    Column("steals",Integer,nullable=True,comment="抄截數"),
    Column("blocks",Integer,nullable=True,comment="阻攻數"),
    Column("turnovers",Integer,nullable=True,comment="失誤數"),
    Column("personal_fouls",Integer,nullable=True,comment="犯規數"),
    Column("points",Integer,nullable=True,comment="得分"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間")
)


# team advance
nba_team_advance_table = Table(
    "nba_team_advance",  # 資料表名稱
    metadata,
    Column("year",Integer,primary_key=True,comment="年度"),
    Column("team",String(50),primary_key=True,comment="球隊名稱"),
    Column("average_age",Float,nullable=True,comment="平均年齡"),
    Column("wins",Integer,nullable=True,comment="勝場數"),
    Column("loses",Integer,nullable=True,comment="敗場數"),
    Column("winsP",Float,nullable=True,comment="勝率"),
    Column("pythagorean_wins",Float,nullable=True,comment="畢氏勝場數"),
    Column("pythagorean_lose",Float,nullable=True,comment="畢氏敗場數"),
    Column("margin_of_victory",Float,nullable=True,comment="勝分差"),
    Column("strength_of_schedule",Float,nullable=True,comment="賽程強度"),
    Column("simple_rating_system",Float,nullable=True,comment="簡易評分系統"),
    Column("offensive_rating",Float,nullable=True,comment="進攻評分"),
    Column("defensive_rating",Float,nullable=True,comment="防守評分"),
    Column("net_rating",Float,nullable=True,comment="淨評分"),
    Column("pace_factor",Float,nullable=True,comment="節奏因子"),
    Column("free_throw_attempt_rate",Float,nullable=True,comment="罰球出手率"),
    Column("3p_attempt_rate",Float,nullable=True,comment="三分球出手率"),
    Column("true_shooting_percentage",Float,nullable=True,comment="真實命中率"),
    Column("effective_field_goal_percentage",Float,nullable=True,comment="有效投籃命中率"),
    Column("turnover_percentage",Float,nullable=True,comment="失誤率"),
    Column("offensive_rebound_percentage",Float,nullable=True,comment="進攻籃板率"),
    Column("free_throws_per_field_goal_attempt",Float,nullable=True,comment="每次投籃出手罰球數"),
    Column("opponent_effective_field_goal_percentage",Float,nullable=True,comment="對手有效投籃命中率"),
    Column("opponent_turnover_percentage",Float,nullable=True,comment="對手失誤率"),
    Column("defensive_rebound_percentage",Float,nullable=True,comment="防守籃板率"),
    Column("opponent_free_throws_per_field_goal_attempt",Float,nullable=True,comment="對手每次投籃出手罰球數"),
    Column("arena_name",String(100),nullable=True,comment="主場館名稱"),
    Column("attendance",Integer,nullable=True,comment="總觀眾人數"),
    Column("attendance_per_g",Float,nullable=True,comment="平均每場觀眾人數"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間")
)

# team merge
nba_team_table = Table(
    "nba_team_table",  # 資料表名稱
    metadata,
    Column("year",Integer,primary_key=True,comment="年度"),
    Column("team",String(50),primary_key=True,comment="球隊名稱"),
    Column("salary",Integer,nullable=True,comment="球隊總薪資"),
    Column("games",Integer,nullable=True,comment="參與比賽數"),
    Column("minutes_played",Integer,nullable=True,comment="總上場時間"),
    Column("field_goals",Integer,nullable=True,comment="投籃命中數"),
    Column("field_goals_attempts",Integer,nullable=True,comment="投籃次數"),
    Column("field_goals_percentage",Float,nullable=True,comment="投籃命中率"),
    Column("3p_field_goals",Integer,nullable=True,comment="三分球命中數"),
    Column("3p_field_goals_attempts",Integer,nullable=True,comment="三分球出手次數"),
    Column("3p_field_goals_percentage",Float,nullable=True,comment="三分球命中率"),
    Column("2p_field_goals",Integer,nullable=True,comment="兩分球命中數"),
    Column("2p_field_goals_attempts",Integer,nullable=True,comment="兩分球出手次數"),
    Column("2p_field_goals_percentage",Float,nullable=True,comment="兩分球命中率"),
    Column("free_throws",Integer,nullable=True,comment="罰球命中數"),
    Column("free_throws_attempts",Integer,nullable=True,comment="罰球出手次數"),
    Column("free_throws_percentage",Float,nullable=True,comment="罰球命中率"),
    Column("offensive_rebounds",Integer,nullable=True,comment="進攻籃板數"),
    Column("defensive_rebounds",Integer,nullable=True,comment="防守籃板數"),
    Column("total_rebounds",Integer,nullable=True,comment="總籃板數"),
    Column("assists",Integer,nullable=True,comment="助攻數"),
    Column("steals",Integer,nullable=True,comment="抄截數"),
    Column("blocks",Integer,nullable=True,comment="阻攻數"),
    Column("turnovers",Integer,nullable=True,comment="失誤數"),
    Column("personal_fouls",Integer,nullable=True,comment="犯規數"),
    Column("points",Integer,nullable=True,comment="得分"),
    Column("average_age",Float,nullable=True,comment="平均年齡"),
    Column("wins",Integer,nullable=True,comment="勝場數"),
    Column("loses",Integer,nullable=True,comment="敗場數"),
    Column("winsP",Float,nullable=True,comment="勝率"),
    Column("pythagorean_wins",Float,nullable=True,comment="畢氏勝場數"),
    Column("pythagorean_lose",Float,nullable=True,comment="畢氏敗場數"),
    Column("margin_of_victory",Float,nullable=True,comment="勝分差"),
    Column("strength_of_schedule",Float,nullable=True,comment="賽程強度"),
    Column("simple_rating_system",Float,nullable=True,comment="簡易評分系統"),
    Column("offensive_rating",Float,nullable=True,comment="進攻評分"),
    Column("defensive_rating",Float,nullable=True,comment="防守評分"),
    Column("net_rating",Float,nullable=True,comment="淨評分"),
    Column("pace_factor",Float,nullable=True,comment="節奏因子"),
    Column("free_throw_attempt_rate",Float,nullable=True,comment="罰球出手率"),
    Column("3p_attempt_rate",Float,nullable=True,comment="三分球出手率"),
    Column("true_shooting_percentage",Float,nullable=True,comment="真實命中率"),
    Column("effective_field_goal_percentage",Float,nullable=True,comment="有效投籃命中率"),
    Column("turnover_percentage",Float,nullable=True,comment="失誤率"),
    Column("offensive_rebound_percentage",Float,nullable=True,comment="進攻籃板率"),
    Column("free_throws_per_field_goal_attempt",Float,nullable=True,comment="每次投籃出手罰球數"),
    Column("opponent_effective_field_goal_percentage",Float,nullable=True,comment="對手有效投籃命中率"),
    Column("opponent_turnover_percentage",Float,nullable=True,comment="對手失誤率"),
    Column("defensive_rebound_percentage",Float,nullable=True,comment="防守籃板率"),
    Column("opponent_free_throws_per_field_goal_attempt",Float,nullable=True,comment="對手每次投籃出手罰球數"),
    Column("arena_name",String(100),nullable=True,comment="主場館名稱"),
    Column("attendance",Integer,nullable=True,comment="總觀眾人數"),
    Column("attendance_per_g",Float,nullable=True,comment="平均每場觀眾人數"),
)

# news 
nba_news_headline_table = Table(
    "nba_news_headline",  # 資料表名稱
    metadata,
    Column("news_at", Date, primary_key=True,comment="新聞取得日期"),
    Column("title",String(100),primary_key=True,comment="新聞頭條標題"),
    Column("article_time", DATETIME,nullable=True,comment="新聞標示時間"),
    Column("label",String(50),nullable=True,comment="新聞頭條分類"),
    Column("link",String(300),nullable=True,comment="新聞頭條網址"),
    Column("uploaded_at", DATETIME,nullable=False,comment="資料上傳時間")
)

nba_news_udn_table = Table(
    "nba_news_udn",  # 資料表名稱
    metadata,
    Column("id", String(100), primary_key=True, comment="新聞ID"),  # 新增新聞ID欄位
    Column("title", String(255), nullable=False, comment="新聞標題"),
    Column("url", String(255), nullable=False, comment="新聞連結"),
    Column("date", String(10), nullable=False, comment="新聞日期"),  # YYYY-MM-DD
    
)   


def upload_data_to_mysql(table_name: str, df: pd.DataFrame, mode: str = "replace"):
    """
    上傳 DataFrame 到 MySQL（使用全域引擎和適當的連接管理）
    """
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)
    
    # 使用 context manager 確保連接會被正確關閉
    with engine.connect() as connection:
        df.to_sql(
            table_name,
            con=connection,
            if_exists=mode,
            index=False,
        )
    print(f"資料已上傳到表 '{table_name}'，共 {len(df)} 筆記錄")


def upload_data_to_mysql_upsert(table_obj: Table, data: list[dict]):
    # 如上，要先建立好資料表，才能作主鍵判斷
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)
    
    # 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine, tables=[table_obj])

    # upsert
    with engine.begin() as connection:
        for row in data:
            insert_stmt = insert(table_obj).values(**row)
            update_dict = {
                col.name: insert_stmt.inserted[col.name]
                for col in table_obj.columns
            }
            upsert_stmt = insert_stmt.on_duplicate_key_update(**update_dict)
            connection.execute(upsert_stmt)
    print(f"UPSERT 完成，處理 {len(data)} 筆記錄到表 '{table_obj.name}'")


def upload_data_to_mysql_insert(table_obj: Table, data: list[dict]):
    """使用 SQLAlchemy INSERT 上傳資料到 MySQL"""
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)
    
    # 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine, tables=[table_obj])
    
    with engine.begin() as connection:
        for row in data:
            insert_stmt = insert(table_obj).values(**row)
            connection.execute(insert_stmt)
    
    print(f"INSERT 完成，處理 {len(data)} 筆記錄到表 '{table_obj.name}'")

def read_data_from_mysql(table_name:str):

    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)

    df = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)

    return df
