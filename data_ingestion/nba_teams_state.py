#儲存2015-2025球隊薪資表格

import urllib.request as req
import bs4 as bs
import pandas as pd
from datetime import datetime, timezone
import os

from data_ingestion.mysql import upload_data_to_mysql, upload_data_to_mysql_upsert, nba_team_state_table




def nba_teams_state(years:list):

    all_rows = []

    for year in years: 

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
        resp = req.urlopen(url)
        content = resp.read()
        html = bs.BeautifulSoup(content, "html.parser")
        print(year)
        table = html.find("div", {"id": "all_totals_team-opponent"}).find("tbody")
        rows = table.find_all("tr")

        for row in rows:
            # 跳過空列或是有 'class=thead' 的分隔列
            if row.get("class") == ['thead']:
                continue

            # 抓球員名字與隊伍代碼
            team = row.find("td", {"data-stat": "team"}).text.strip().replace('*', '')
            g = row.find("td", {"data-stat": "g"}).text.strip()
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
                "team": team,
                "games": g,
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

            int_columns = ['year','games',"minutes_played","field_goals","field_goals_attempts",
                           "3p_field_goals","3p_field_goals_attempts",
                           "2p_field_goals","2p_field_goals_attempts",
                           "free_throws","free_throws_attempts",
                           "offensive_rebounds","defensive_rebounds","total_rebounds","assists",
                           "steals","blocks","turnovers","personal_fouls","points"]
            float_columns = ["field_goals_percentage",'3p_field_goals_percentage',
                             "2p_field_goals_percentage","free_throws_percentage"]



            data = convert_fields(data, int_fields=int_columns, float_fields=float_columns)

            all_rows.append(data)



    df = pd.DataFrame(all_rows)
  
    
    df['uploaded_at'] = datetime.now(timezone.utc)
    
    dirname = "output"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    # save
    df.to_csv(f'output/nba_teams_state.csv', index=False, encoding="utf-8-sig")

    # to MySQL
    
    # upload_data_to_mysql(table_name = 'nba_teams_state', df=df, mode = 'replace')

    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_team_state_table, all_rows)
    print(f"nba_teams_state has been uploaded to mysql.")


   
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


#%%

if __name__ == '__main__':

    years = list(range(2015,2026))


    nba_teams_state(years)

