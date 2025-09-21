"""
Filename:    scawler_salary.py
Author:      Shin Yuan Huang
Created:     2025-07-30 
Description: NBA salary data from www.hoopshype.com
"""

import urllib.request as req
import bs4 as bs
import pandas as pd
import time
from datetime import datetime, timezone
import random
import unicodedata
import re
import os
from data_ingestion.mysql import  upload_data_to_mysql_upsert, nba_player_salary_table


#%% function
def player_year_salary(year:int):
    
    team_inf = {
        'atlanta-hawks': [1],
        'boston-celtics': [2],
        'brooklyn-nets': [17],
        'charlotte-hornets': [5312],
        'chicago-bulls': [4],
        'cleveland-cavaliers': [5],
        'dallas-mavericks': [6],
        'denver-nuggets': [7],
        'detroit-pistons': [8],
        'golden-state-warriors': [9],
        'houston-rockets': [10],
        'indiana-pacers': [11],
        'los-angeles-clippers': [12],
        'los-angeles-lakers': [13],
        'memphis-grizzlies': [29],
        'miami-heat': [14],
        'milwaukee-bucks': [15],
        'minnesota-timberwolves': [16],
        'new-orleans-pelicans': [3],
        'new-york-knicks': [18],
        'oklahoma-city-thunder': [25],
        'orlando-magic': [19],
        'philadelphia-76ers': [20],
        'phoenix-suns': [21],
        'portland-trail-blazers': [22],
        'sacramento-kings': [23],
        'san-antonio-spurs': [24],
        'toronto-raptors': [28],
        'utah-jazz': [26],
        'washington-wizards': [27]
    }


    all_raws = []

    for team_name, url_num in team_inf.items():

        url = f"https://www.hoopshype.com/salaries/teams/{team_name}/{url_num[0]}/?season={year}"
        # print(url)

        # 儲存的路徑
        # dirname = os.path.join('.', 'salary')
        # if not os.path.exists(dirname):
        #     os.makedirs(dirname)

        # 取得網頁內容
        r = req.Request(url)
        r.add_header('user-agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')

        # 開啟網址並讀取html內容
        resp = req.urlopen(r)
        content = resp.read()
        html = bs.BeautifulSoup(content,'html.parser')
        print(f"{year} {team_name}")

        # players
        players = html.find_all('td', {"class": "vTd-Ji__vTd-Ji"})
        player_list = []
        for player in players:
            player_list.append(remove_accents_and_symbols_keep_space(player.text))
        player_list = player_list[:-1]
        # player_list[-1] = 'total'

        # salary
        year_items = html.find_all('th', {"colspan": "1", "class": "RLrCiX__RLrCiX"})
        salaryAll = html.find_all('td', {"class": "RLrCiX__RLrCiX"})
        salary_list = []
        for salary in salaryAll:
            salary_list.append(int(salary.text.strip()[1:].replace(',', '')))
        salary_list = salary_list[:-len(year_items)][::len(year_items)]

        for i in range(len(player_list)):
            all_raws.append({
                'year': year+1,
                'team': team_name,
                'player': player_list[i],
                'salary': salary_list[i],
                'uploaded_at': datetime.now(timezone.utc)
            })

        time.sleep(random.uniform(3, 5))  # 輕微延遲，避免封鎖


    df = pd.DataFrame(all_raws)
    # print(df)
   

    dirname = "output"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    # save
    df.to_csv(f'output/{year+1}_nba_players_salary.csv', index=False, encoding="utf-8-sig")
    # with open('salary.json', 'w', encoding='utf-8') as f:
    #     json.dump(row, f, indent=4, ensure_ascii=False)

    # to mySQL
    # upload_data_to_mysql(table_name = 'nba_players_salary', df=df, mode = 'replace')
    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_player_salary_table, all_raws)

    print(f"nba_players_salary has been uploaded to mysql.")


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
#%%

if __name__ == '__main__':

    years = list(range(2014,2025))

    for i in years:

        player_year_salary(i)

