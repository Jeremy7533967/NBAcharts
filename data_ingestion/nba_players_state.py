
import urllib.request as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from datetime import datetime, timezone
import random
import unicodedata
import re
import os

from data_ingestion.mysql import  upload_data_to_mysql_upsert, nba_player_state_table



def nba_players_state(years:list):

    rows_all = []

    for year in years:

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
        print(url)

        # 建立 Request 並加上 headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        req_obj = req.Request(url, headers=headers)

        # 發送請求
        resp = req.urlopen(req_obj)
        content = resp.read()
        html = bs(content, 'html.parser')

        table = html.find("tbody")
        rows = table.find_all("tr")
            
        for row in rows:
        # 跳過空列或是有 'class=thead' 的分隔列
            if row.get("class") == ['thead']:
                continue
            if row.find("td", {"data-stat": "name_display"}).text.strip() == 'League Average':
                continue
            if row.find("td", {"data-stat": "team_name_abbr"}).text.strip() == '2TM':
                continue
            if row.find("td", {"data-stat": "team_name_abbr"}).text.strip() == '3TM':
                continue
            if row.find("td", {"data-stat": "team_name_abbr"}).text.strip() == '4TM':
                continue

            # 抓球員名字與隊伍代碼
            name = row.find("td", {"data-stat": "name_display"}).text.strip()
            age = row.find("td", {"data-stat": "age"}).text.strip()
            team = row.find("td", {"data-stat": "team_name_abbr"}).text.strip()
            pos = row.find("td", {"data-stat": "pos"}).text.strip()
            g = row.find("td", {"data-stat": "games"}).text.strip()
            gs = row.find("td", {"data-stat": "games_started"}).text.strip()
            mp = row.find("td", {"data-stat": "mp"}).text.strip()
            fg = row.find("td", {"data-stat": "fg"}).text.strip()
            fga = row.find("td", {"data-stat": "fga"}).text.strip()
            fg_pct = row.find("td", {"data-stat": "fg_pct"}).text.strip()
            p3 = row.find("td", {"data-stat": "fg3"}).text.strip()
            pa3 = row.find("td", {"data-stat": "fg3a"}).text.strip()
            p3_pct = row.find("td", {"data-stat": "fg3_pct"}).text.strip()
            p2 = row.find("td", {"data-stat": "fg2"}).text.strip()
            pa2 = row.find("td", {"data-stat": "fg2a"}).text.strip()
            p2_pct = row.find("td", {"data-stat": "fg2_pct"}).text.strip()
            efg_pct = row.find("td", {"data-stat": "efg_pct"}).text.strip()
            e_fga_pct = row.find("td", {"data-stat": "efg_pct"}).text.strip()
            ft = row.find("td", {"data-stat": "ft"}).text.strip()
            fta = row.find("td", {"data-stat": "fta"}).text.strip()
            ft_pct = row.find("td", {"data-stat": "ft_pct"}).text.strip()
            orb = row.find("td", {"data-stat": "orb"}).text.strip()
            drb = row.find("td", {"data-stat": "drb"}).text.strip()
            trb = row.find("td", {"data-stat": "trb"}).text.strip()
            ast = row.find("td", {"data-stat": "ast"}).text.strip()
            stl = row.find("td", {"data-stat": "stl"}).text.strip()
            blk = row.find("td", {"data-stat": "blk"}).text.strip()
            tov = row.find("td", {"data-stat": "tov"}).text.strip()
            pf = row.find("td", {"data-stat": "pf"}).text.strip()
            pts = row.find("td", {"data-stat": "pts"}).text.strip()

            data = replace_empty_with_none({
                    "year": year,
                    "player": remove_accents_and_symbols_keep_space(name),
                    "team": team,
                    "age": age,
                    "pos": pos,
                    "games": g,
                    "games_started": gs,
                    "minutes_played": mp,
                    "field_goals": fg,
                    "field_goals_attempts": fga,
                    "field_goals_percentage": fg_pct,
                    "3p_field_goals": p3,
                    "3p_field_goals_attempts": pa3,
                    "3p_field_goals_percentage": p3_pct,
                    "2p_field_goals": p2,
                    "2p_field_goals_attempts": pa2,
                    "2p_field_goals_percentage": p2_pct,
                    "efg_pct": efg_pct,
                    "free_throws": ft,
                    "free_throws_attempts": fta,
                    "free_throws_percentage": ft_pct,
                    "offensive_rebounds": orb,
                    "defensive_rebounds": drb,
                    "total_rebounds": trb,
                    "assists": ast,
                    "steals": stl,
                    "blocks": blk,
                    "turnovers": tov,
                    "personal_fouls": pf,
                    "points":pts,
                    "uploaded_at":datetime.now(timezone.utc)
                    })
            
            int_columns = ['year','age', 'games', 'games_started',"minutes_played",
                           "field_goals","field_goals_attempts","3p_field_goals","3p_field_goals_attempts",
                           "2p_field_goals","2p_field_goals_attempts","free_throws","free_throws_attempts",
                           "offensive_rebounds","defensive_rebounds","total_rebounds","assists",
                           "steals","blocks","turnovers","personal_fouls","points"]
            float_columns = ["field_goals_percentage",'field_goals_percentage', '3p_field_goals_percentage',
                             "2p_field_goals_percentage","efg_pct","free_throws_percentage"]

            data = convert_fields(data, int_fields=int_columns, float_fields=float_columns)

            rows_all.append(data)

        time.sleep(random.uniform(5, 10))  # 輕微延遲，避免封鎖
            

    dirname = "output"
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    df = pd.DataFrame(rows_all)
    # df.replace('', 0,  inplace=True)  # 將空字串補成 0，以利轉換資料型態


    df.drop(df.index[-1], inplace=True) # 移除最後一列平均值
    # df.index += 1
    df['uploaded_at'] = datetime.now(timezone.utc)

    # save
    # fn = os.path.join(dirname, f"nba_players_state_{year}.csv")
    df.to_csv(f'output/nba_players_state.csv', index=False, encoding="utf-8-sig")

    # to MySQL
    
    # upload_data_to_mysql(table_name = 'nba_players_state', df=df, mode = 'replace')

    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_player_state_table, rows_all)
    print(f"nba_players_state has been uploaded to mysql.")

   
def replace_empty_with_none(data_dict):
    """
    將字典中所有 value 為 '' 的項目替換成 None。
    
    參數：
        data_dict (dict): 要處理的原始字典。
    
    回傳：
        dict: 處理後的字典（原地修改）。
    """
    for k, v in data_dict.items():
        if v == '':
            data_dict[k] = None
    return data_dict

def convert_fields(data, int_fields=None, float_fields=None):
    """
    將指定欄位轉成 int 或 float 型別，如果遇到 None 或空字串就跳過。
    """
    int_fields = int_fields or []
    float_fields = float_fields or []

    for key in int_fields:
        if key in data and data[key] not in (None, ''):
            try:
                data[key] = int(data[key])
            except ValueError:
                pass  # 或 raise 自己看要不要丟錯

    for key in float_fields:
        if key in data and data[key] not in (None, ''):
            try:
                data[key] = float(data[key])
            except ValueError:
                pass

    return data


def remove_accents_and_symbols_keep_space(text):
    """
    去除重音符號與所有非英數和空格的符號，保留空格與 a-zA-Z0-9。
    """
    if not isinstance(text, str):
        return text

    # 1. 正規化文字（去除重音符）
    normalized = unicodedata.normalize('NFKD', text)
    text_no_accents = ''.join([c for c in normalized if not unicodedata.combining(c)])

    # 2. 移除所有非英數字與空格（保留 a-zA-Z0-9 和空格）
    text_clean = re.sub(r'[^A-Za-z0-9 ]', '', text_no_accents)

    return text_clean



if __name__ == '__main__':

    years = list(range(2015,2026))

    nba_players_state(years)

# print(nba_players_state(2020))
