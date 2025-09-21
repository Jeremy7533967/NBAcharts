
import requests
import urllib.request as req
import bs4 as bs
import pandas as pd
import time
import random
import os
from datetime import datetime, timezone

from data_ingestion.mysql import upload_data_to_mysql, upload_data_to_mysql_upsert, nba_team_salary_table



def nba_teams_salary(years: list):

    all_raws = []

    for year in years: 

        url = f'https://www.hoopshype.com/salaries/teams/?season={year}'


        r = req.Request(url)
        r.add_header('user-agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')

        # 開啟網址並讀取html內容
        resp = req.urlopen(r)
        content = resp.read()
        html = bs.BeautifulSoup(content,'html.parser')
        print(year)

        # teams
        teams = html.find_all('div', {"class": "_0cD6l-__0cD6l-"})
        teams_list = []
        for team in teams:
            teams_list.append(team.text.strip())

        # salaries
        salaries = html.find_all('td', {"class": "RLrCiX__RLrCiX"})
        salaries_list = []
        for salary in salaries:
            salaries_list.append(int(salary.text.strip()[1:].replace(',', '')))


        for i in range(len(teams_list)):
            all_raws.append({
                'year': year+1,
                'team': teams_list[i],
                'salary': salaries_list[i],
                'uploaded_at': datetime.now(timezone.utc)
            })

        time.sleep(random.uniform(1, 3))  # 輕微延遲，避免封鎖

    df = pd.DataFrame(all_raws)

    dirname = "output"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    
    # save
    df.to_csv(f'output/nba_teams_salary.csv', index=False, encoding="utf-8-sig")

    
    # to mySQL
    # upload_data_to_mysql(table_name = 'nba_teams_salary', df=df, mode = 'replace')
    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_team_salary_table, all_raws)
    
    print(f"nba_teams_salary has been uploaded to mysql.")



if __name__ == '__main__':

    years = list(range(2014,2025))

    nba_teams_salary(years)

# print(nba_teams_salary(2001))
