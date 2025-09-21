
import urllib.request as req
import os
import bs4 as bs
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from data_ingestion.mysql import upload_data_to_mysql, upload_data_to_mysql_upsert, nba_team_advance_table



def nba_teams_advancedstate(years:list):

    all_rows = []

    for year in years:

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
        print(year)
        resp = req.urlopen(url)
        content = resp.read()
        html = bs.BeautifulSoup(content,'html.parser')

        table = html.find("div", {"id": "all_advanced_team"}).find("tbody")
        rows = table.find_all("tr")

        team_seen = set()

        for row in rows:
            # 跳過空列或是有 'class=thead' 的分隔列
            if row.get("class") == ['thead']:
                continue

            # 抓球員名字與隊伍代碼
            team_cell = row.find("td", {"data-stat": "team"})
            age_cell = row.find("td", {"data-stat": "age"})
            wins_cell = row.find("td", {"data-stat": "wins"})
            losses_cell = row.find("td", {"data-stat": "losses"})
            wins_pyth_cell = row.find("td", {"data-stat": "wins_pyth"})
            losses_pyth_cell = row.find("td", {"data-stat": "losses_pyth"})
            mov_cell = row.find("td", {"data-stat": "mov"})
            sos_cell = row.find("td", {"data-stat": "sos"})
            srs_cell = row.find("td", {"data-stat": "srs"})
            off_rtg_cell = row.find("td", {"data-stat": "off_rtg"})
            def_rtg_cell = row.find("td", {"data-stat": "def_rtg"})
            net_rtg_cell = row.find("td", {"data-stat": "net_rtg"})
            pace_cell = row.find("td", {"data-stat": "pace"})
            fta_per_fga_pct_cell = row.find("td", {"data-stat": "fta_per_fga_pct"})
            fg3a_per_fga_pct_cell = row.find("td", {"data-stat": "fg3a_per_fga_pct"})
            ts_pct_cell = row.find("td", {"data-stat": "ts_pct"})
            efg_pct_cell = row.find("td", {"data-stat": "efg_pct"})
            tov_pct_cell = row.find("td", {"data-stat": "tov_pct"})
            orb_pct_cell = row.find("td", {"data-stat": "orb_pct"})
            ft_rate_cell = row.find("td", {"data-stat": "ft_rate"})
            opp_efg_pct_cell = row.find("td", {"data-stat": "opp_efg_pct"})
            opp_tov_pct_cell = row.find("td", {"data-stat": "opp_tov_pct"})
            drb_pct_cell = row.find("td", {"data-stat": "drb_pct"})
            opp_ft_rate_cell = row.find("td", {"data-stat": "opp_ft_rate"})
            arena_name_cell = row.find("td", {"data-stat": "arena_name"})
            attendance_cell = row.find("td", {"data-stat": "attendance"})
            attendance_per_g_cell = row.find("td", {"data-stat": "attendance_per_g"})


            team = team_cell.text.replace('*', '').strip()
            age = age_cell.text.strip()
            wins = wins_cell.text.strip()
            losses = losses_cell.text.strip()
            wins_pyth = wins_pyth_cell.text.strip()
            losses_pyth = losses_pyth_cell.text.strip()
            mov = mov_cell.text.strip()
            sos = sos_cell.text.strip()
            srs = srs_cell.text.strip()
            off_rtg = off_rtg_cell.text.strip()
            def_rtg = def_rtg_cell.text.strip()
            net_rtg = net_rtg_cell.text.strip()
            pace = pace_cell.text.strip()
            fta_per_fga_pct = fta_per_fga_pct_cell.text.strip()
            fg3a_per_fga_pct = fg3a_per_fga_pct_cell.text.strip()
            ts_pct = ts_pct_cell.text.strip()
            efg_pct = efg_pct_cell.text.strip()
            tov_pct = tov_pct_cell.text.strip()
            orb_pct = orb_pct_cell.text.strip()
            ft_rate = ft_rate_cell.text.strip()

            opp_efg_pct = opp_efg_pct_cell.text.strip()
            opp_tov_pct = opp_tov_pct_cell.text.strip()
            drb_pct = drb_pct_cell.text.strip()
            opp_ft_rate = opp_ft_rate_cell.text.strip()

            arena_name = arena_name_cell.text.strip()

            attendance = attendance_cell.text.strip().replace(',', '')
            if attendance == '':
                attendance = None
            else:
                attendance = int(attendance)

            attendance_per_g = attendance_per_g_cell.text.strip().replace(',', '')
            if attendance_per_g == '':
                attendance_per_g = None
            else:
                attendance_per_g = float(attendance_per_g)


            all_rows.append({
                "year": year,
                "team": team,
                "average_age": float(age),
                "wins": int(wins),
                "loses": int(losses),
                "winsP": float(int(wins)/(int(losses)+int(wins))),
                "pythagorean_wins": float(wins_pyth),
                "pythagorean_lose": float(losses_pyth),
                "margin_of_victory": float(mov),
                "strength_of_schedule": float(sos),
                "simple_rating_system": float(srs),
                "offensive_rating": float(off_rtg),
                "defensive_rating": float(def_rtg),
                "net_rating": float(net_rtg),
                "pace_factor": float(pace),
                "free_throw_attempt_rate": float(fta_per_fga_pct),
                "3p_attempt_rate": float(fg3a_per_fga_pct),
                "true_shooting_percentage": float(ts_pct),
                "effective_field_goal_percentage": float(efg_pct),
                "turnover_percentage": float(tov_pct),
                "offensive_rebound_percentage": float(orb_pct),
                "free_throws_per_field_goal_attempt": float(ft_rate),

                "opponent_effective_field_goal_percentage": float(opp_efg_pct),
                "opponent_turnover_percentage": float(opp_tov_pct),
                "defensive_rebound_percentage": float(drb_pct),
                "opponent_free_throws_per_field_goal_attempt": float(opp_ft_rate),

                "arena_name": arena_name,
                "attendance": attendance,
                "attendance_per_g": attendance_per_g,

                "uploaded_at": datetime.now(timezone.utc)

                })


    df = pd.DataFrame(all_rows)
  
    # df['attendance'] = df['attendance'].str.replace(',', '', regex=False).astype(int)
    # df['attendance_per_g'] = df['attendance_per_g'].str.replace(',', '', regex=False).astype(float)
    # df.replace('', 0,  inplace=True)  # 將空字串補成 0，以利轉換資料型態
    # df.index += 1
    df["uploaded_at"] = datetime.now(timezone.utc)

    dirname = "output"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    # save
    df.to_csv(f'output/nba_teams_advancedstate.csv', index=False, encoding="utf-8-sig")

    # to MySQL
    
    # upload_data_to_mysql(table_name = 'nba_teams_advance', df=df, mode = 'replace')

    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_team_advance_table, all_rows)
    print(f"nba_teams_advance has been uploaded to mysql.")

    

if __name__ == '__main__':

    years = list(range(2015,2026))

    nba_teams_advancedstate(years)


