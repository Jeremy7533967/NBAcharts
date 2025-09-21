import urllib.request as req
import bs4 as bs
import pandas as pd
import time
import random

from data_ingestion.worker import app
@app.task()

def player_year_salary(year):

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

    all_rows = []

    for team_name, url_num in team_inf.items():

        url = f"https://www.hoopshype.com/salaries/teams/{team_name}/{url_num[0]}/?season={year}"
        print(url)


        # 取得網頁內容
        r = req.Request(url)
        r.add_header('user-agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')

        # 開啟網址並讀取html內容
        resp = req.urlopen(r)
        content = resp.read()
        html = bs.BeautifulSoup(content)


        # players
        players = html.find_all('td', {"class": "vTd-Ji__vTd-Ji"})
        player_list = []
        for player in players:
            player_list.append(player.text)
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
            all_rows.append({
                'year': year,
                'team': team_name,
                'players': player_list[i],
                'salary': salary_list[i]
            })

        time.sleep(random.uniform(3, 5))  # 輕微延遲，避免封鎖


    df = pd.DataFrame(all_rows)

    # save
    df.to_csv(f'output/salary_{year}_playeres.csv', index=False)

