
import pandas as pd
from data_ingestion.mysql import read_data_from_mysql, upload_data_to_mysql_upsert, nba_team_table, nba_player_table



def team_name_convert(df):

    nba_teams_fullname = {
        "atlanta-hawks": ["ATL", "Hawks", "Atlanta Hawks"],
        "boston-celtics": ["BOS", "Celtics", "Boston Celtics"],
        "brooklyn-nets": ["BRK", "Nets", "Brooklyn Nets"],
        "charlotte-hornets": ["CHO", "Hornets", "Charlotte Hornets"],
        "chicago-bulls": ["CHI", "Bulls", "Chicago Bulls"],
        "cleveland-cavaliers": ["CLE", "Cavaliers", "Cleveland Cavaliers"],
        "dallas-mavericks": ["DAL", "Mavericks", "Dallas Mavericks"],
        "denver-nuggets": ["DEN", "Nuggets", "Denver Nuggets"],
        "detroit-pistons": ["DET", "Pistons", "Detroit Pistons"],
        "golden-state-warriors": ["GSW", "Warriors", "Golden State Warriors"],
        "houston-rockets": ["HOU", "Rockets", "Houston Rockets"],
        "indiana-pacers": ["IND", "Pacers", "Indiana Pacers"],
        "los-angeles-clippers": ["LAC", "Clippers", "Los Angeles Clippers"],
        "los-angeles-lakers": ["LAL", "Lakers", "Los Angeles Lakers"],
        "memphis-grizzlies": ["MEM", "Grizzlies", "Memphis Grizzlies"],
        "miami-heat": ["MIA", "Heat", "Miami Heat"],
        "milwaukee-bucks": ["MIL", "Bucks", "Milwaukee Bucks"],
        "minnesota-timberwolves": ["MIN", "Timberwolves", "Minnesota Timberwolves"],
        "new-orleans-pelicans": ["NOP", "Pelicans", "New Orleans Pelicans"],
        "new-york-knicks": ["NYK", "Knicks", "New York Knicks"],
        "oklahoma-city-thunder": ["OKC", "Thunder", "Oklahoma City Thunder"],
        "orlando-magic": ["ORL", "Magic", "Orlando Magic"],
        "philadelphia-76ers": ["PHI", "76ers", "Philadelphia 76ers"],
        "phoenix-suns": ["PHO", "Suns", "Phoenix Suns"],
        "portland-trail-blazers": ["POR", "Trail Blazers", "Portland Trail Blazers"],
        "sacramento-kings": ["SAC", "Kings", "Sacramento Kings"],
        "san-antonio-spurs": ["SAS", "Spurs", "San Antonio Spurs"],
        "toronto-raptors": ["TOR", "Raptors", "Toronto Raptors"],
        "utah-jazz": ["UTA", "Jazz", "Utah Jazz"],
        "washington-wizards": ["WAS", "Wizards", "Washington Wizards"]
    }



    # 建立反查字典
    name_to_full = {}
    for full_name, aliases in nba_teams_fullname.items():
        name_to_full[full_name] = full_name
        for alias in aliases:
            name_to_full[alias] = full_name 


    df["team"] = df["team"].map(name_to_full).fillna(df["team"])

    return df

def player_name_convert(df):

    nba_player_fullname = {
        "Antonius Cleveland": ["A Cleveland"],
        "Aleksej Pokusevski": ["A Pokusevski"],
        "Admiral Schofield": ["A Schofield"],
        "Amare Stoudemire": ["A Stoudemire"],
        "Andrew White III": ['Andrew White'],
        "Anthony Barber": ["Cat Barber"],
        "Bogdan Bogdanovic": ["B Bogdanovic"],
        "Bryce DejeanJones": ["B DejeanJones"],
        "Billy Garrett": ["B Garrett"],
        "Bennedict Mathurin": ["B Mathurin"],
        "Brandin Podziemski": ["B Podziemski"],
        "Baylor Scheierman": ["B Scheierman"],
        "Brandon Boston Jr": ["BJ Boston"],
        "Brian Bowen II": ["Brian Bowen"],
        "Bub Carrington": ["C Carrington"],
        "Charlie Brown Jr": ["C Brown"],
        "Chris DouglasRoberts": ["C DouglasRoberts"],
        "Cristiano Felicio": ["C Felicio"],
        "Chandler Hutchison": ["C Hutchison"],
        "Chris Johnson": ["C Johnson"],
        "Charlie Villanueva": ["C Villanueva"],
        "Craig Porter Jr": ["Craig Porter"],
        "DeVaughn AkoonPurcell": ["D AkoonPurcell"],
        "Dorian FinneySmith": ["D FinneySmith"],
        "Demetrius Jackson": ["D Jackson"],
        "Derrick Jones Jr": ["D Jones"],
        "DeAnthony Melton": ["D Melton"],
        "Donatas Motiejunas": ["D Motiejunas"],
        "Deividas Sirvydis": ["D Sirvydis"],
        "Dmytro Skapintsev": ["D Skapintsev"],
        "Derrick Walton": ["D Walton"],
        "Duane Washington Jr": ["D Washington"],
        "Dereck Lively II": ["Dereck Lively"],
        "Elijah Harkless": ["EJ Harkless"],
        "Freddie Gillespie": ["F Gillespie"],
        "Frank Kaminsky": ["F Kaminsky"],
        "Giannis Antetokounmpo": ["G Antetokounmpo"],
        "Georgios Kalaitzakis": ["G Kalaitzakis"],
        "Georgios Papagiannis": ["G Papagiannis"],
        "Glenn Robinson III": ["G Robinson"],
        "Guerschon Yabusele": ["G Yabusele"],
        "GG Jackson II": ["GG Jackson"],
        "Greg Brown III": ["Greg Brown"],
        "Haywood Highsmith": ["H Highsmith"],
        "Harry Giles III": ["Harry Giles"],
        "Hidayet Turkoglu": ["Hedo Turkoglu"],
        "Izaiah Brockington": ["I Brockington"],
        "Isaiah Hartenstein": ["I Hartenstein"],
        "Immanuel Quickley": ["I Quickley"],
        "Ishmael Smith": ["Ish Smith"],
        "Ish Wainright": ["I Wainright"],
        "Jaron Blossomgame": ["J Blossomgame"],
        "Justin Champagnie": ["J Champagnie"],
        "Jarron Cumberland": ["J Cumberland"],
        "Javon FreemanLiberty": ["J FreemanLiberty"],
        "Juancho Hernangomez": ["J Hernangomez"],
        "Jalen HoodSchifino": ["J HoodSchifino"],
        "Joffrey Lauvergne": ["J Lauvergne"],
        "Jordan McLaughlin": ["J McLaughlin"],
        "James Michael McAdoo": ["J Michael"],
        "Johnny OBryant": ["J OBryant"],
        "Jeremiah RobinsonEarl": ["J RobinsonEarl"],
        "Juan ToscanoAnderson": ["J ToscanoAnderson"],
        "Jonas Valanciunas": ["J Valanciunas"],
        "Jarred Vanderbilt": ["J Vanderbilt"],
        "Johnathan Williams": ["J Williams"],
        "Justin WrightForeman": ["J WrightForeman"],
        "Jabari Smith Jr": ["Jabari Smith"],
        "Jacob Evans III": ["Jacob Evans"],
        "Jaime Jaquez Jr": ["Jaime Jaquez"],
        "James Webb III": ["James Webb"],
        "Jeff Dowtin Jr": ["Jeff Dowtin"],
        "Jeffery Taylor": ["Jeff Taylor"],
        "Joshua Primo": ["Josh Primo"],
        "Jose Juan Barea": ["JJ Barea"],
        "Kostas Antetokounmpo": ["K Antetokounmpo"],
        "Kentavious CaldwellPope": ["K CaldwellPope"],
        "Kyle Collinsworth": ["K Collinsworth"],
        "Kenneth Lofton Jr": ["K Lofton"],
        "Kevin McCullar Jr": ["K McCullar"],
        "Kostas Papanikolaou": ["K Papanikolaou"],
        "Kristaps Porzingis": ["K Porzingis"],
        "KarlAnthony Towns": ["K Towns"],
        "Kevin Knox II": ["Kevin Knox"],
        "LaMarcus Aldridge": ["L Aldridge"],
        "Louis Amundson": ["Lou Amundson"],
        "Langston Galloway": ["L Galloway"],
        "Luc Mbah a Moute": ["L Richard"],
        "Lindell Wigginton": ["L Wigginton"],
        "Louis Williams": ["Lou Williams"],
        "Marvin Bagley III": ["M Bagley"],
        "Michael CarterWilliams": ["M CarterWilliams"],
        "Matthew Dellavedova": ["M Dellavedova"],
        "Marcus Derrickson": ["M Derrickson"],
        "Melvin Frazier": ["M Frazier"],
        "Marcus GeorgesHunt": ["M GeorgesHunt"],
        "Mfiondu Kabengele": ["M Kabengele"],
        "Michael KiddGilchrist": ["M KiddGilchrist"],
        "Mindaugas Kuzminskas": ["M Kuzminskas"],
        "Marcus Morris": ["M Morris"],
        "Michael Porter Jr": ["M Porter"],
        "Miroslav Raduljica": ["M Raduljica"],
        "Malachi Richardson": ["M Richardson"],
        "Mitchell Robinson": ["M Robinson"],
        "Marreese Speights": ["M Speights"],
        "Marcus Thornton": ["M Thornton"],
        "Matt Williams": ["M Williams"],
        "Metta World Peace": ["M World"],
        "McKinley Wright IV": ["M Wright"],
        "MarJon Beauchamp": ["Marjon Beauchamp"],
        "Michael Foster Jr": ["Michael Foster"],
        "Maurice Williams": ["Mo Williams"],
        "Nickeil AlexanderWalker": ["N AlexanderWalker"],
        "Nicolas Laprovittola": ["N Laprovittola"],
        "Nigel WilliamsGoss": ["N WilliamsGoss"],
        "Nene Hilario": ["Nene"],
        "Nick Smith Jr": ["Nick Smith"],
        "Nigel HayesDavis": ["Nigel Hayes"],
        "OlivierMaxence Prosper": ["O Prosper"],
        "Omer Asik": ["Omer Ask"],
        "Patrick Baldwin Jr": ["P Baldwin"],
        "Patrick Patterson": ["P Patterson"],
        "Patrick Mills": ["Patty Mills"],
        "Quinndary Weatherspoon": ["Q Weatherspoon"],
        "Reggie Bullock": ["R Bullock"],
        "Rondae HollisJefferson": ["R HollisJefferson"],
        "Richard Jefferson": ["R Jefferson"],
        "Russell Westbrook": ["R Westbrook"],
        "RJ Nembhard Jr": ["RJ Nembhard"],
        "Raymond Spalding": ["Ray Spalding"],
        "Robert Woodard II": ["Robert Woodard"],
        "Spencer Dinwiddie": ["S Dinwiddie"],
        "Simone Fontecchio": ["S Fontecchio"],
        "Shai GilgeousAlexander": ["S GilgeousAlexander"],
        "Shaquille Harrison": ["S Harrison"],
        "Sandro Mamukelashvili": ["S Mamukelashvili"],
        "Svi Mykhailiuk": ["S Mykhailiuk"],
        "Scotty Pippen Jr": ["S Pippen"],
        "Sebastian Telfair": ["S Telfair"],
        "Sindarius Thornwell": ["S Thornwell"],
        "Shayne Whittington": ["S Whittington"],
        "Stephen Zimmerman": ["S Zimmerman"],
        "TyShon Alexander": ["T Alexander"],
        "Thanasis Antetokounmpo": ["T Antetokounmpo"],
        "Terrance Ferguson": ["T Ferguson"],
        "Tyrese Haliburton": ["T Haliburton"],
        "Talen HortonTucker": ["T HortonTucker"],
        "Trayce JacksonDavis": ["T JacksonDavis"],
        "Timothe LuwawuCabarrot": ["T LuwawuCabarrot"],
        "Trey McKinneyJones": ["T McKinneyJones"],
        "Terrence Shannon Jr": ["T Shannon"],
        "TyTy Washington Jr": ["T Washington"],
        "Trey Murphy III": ["Trey Murphy"],
        "Victor Wembanyama": ["V Wembanyama"],
        "Vince Williams Jr": ["V Williams"],
        "Vernon Carey Jr": ["Vernon Carey"],
        "Wendell Carter Jr": ["W Carter", "Wendell Carter"],
        "Willie CauleyStein": ["W CauleyStein"],
        "Willy Hernangomez": ["W Hernangomez"],
        "Wendell Moore Jr": ["W Moore"],
        "Wade Baldwin IV": ["Wade Baldwin"],
        "Walter Lemon Jr": ["Walt Lemon Jr"],
        "Wayne Selden Jr": ["Wayne Selden"],
        "Wesley Iwundu": ["Wes Iwundu"],
        "Walter Tavares": ["Edy Tavares"],
        "Xavier RathanMayes": ["X RathanMayes"],
        "Xavier Tillman Sr": ["Xavier Tillman"],
        "Zaccharie Risacher": ["Z Risacher"],
    }



    # 建立反查字典
    name_to_full = {}
    for full_name, aliases in nba_player_fullname.items():
        name_to_full[full_name] = full_name
        for alias in aliases:
            name_to_full[alias] = full_name 


    df["player"] = df["player"].map(name_to_full).fillna(df["player"])

    return df

def team_data_merge():

    df_team_salary = team_name_convert(read_data_from_mysql('nba_team_salary')).drop('uploaded_at', axis=1)
    df_team_state = team_name_convert(read_data_from_mysql('nba_team_state')).drop('uploaded_at', axis=1)
    df_team_adv = team_name_convert(read_data_from_mysql('nba_team_advance')).drop('uploaded_at', axis=1)

    merged_1 = pd.merge(df_team_salary, df_team_state, on=['year', 'team'], how='inner')
    df_merged = pd.merge(merged_1, df_team_adv, on=['year', 'team'], how='inner')
    
    df = df_merged.copy()
    df = df.where(pd.notnull(df), None)

    data = df.to_dict(orient='records')

    # 確保所有 nan 都變成 None
    for row in data:
        for k, v in row.items():
            if isinstance(v, float) and pd.isna(v):
                row[k] = None 
    
    
    upload_data_to_mysql_upsert(nba_team_table, data)

def player_data_merge():
    df_player_salary = team_name_convert(read_data_from_mysql('nba_player_salary')).drop('uploaded_at', axis=1)
    df_player_state = team_name_convert(read_data_from_mysql('nba_player_state')).drop('uploaded_at', axis=1)

    # df_salary = []
    # for i in range(2015,2026):
    #     df_salary.append(pd.read_csv(f'/home/amy/01_shinyuan/output/{i}_nba_players_salary.csv'))
    # df_salary = pd.concat(df_salary)
    # df_state = pd.read_csv('/home/amy/01_shinyuan/output/nba_players_state.csv')
    # df = df.sort_values(by=['player', 'year'])


    # 球員名稱轉換
    df_player_salary = player_name_convert(df_player_salary)
    df_player_state = player_name_convert(df_player_state)


    # 以 'year', 'team', 'player' 為 key，做 outer join
    df_merged = pd.merge(df_player_salary, df_player_state,
                        on=['year', 'team', 'player'],
                        how='outer')

    # # 找出 year+player 組合重複的資料
    # dup_mask = df_merged.duplicated(subset=['year', 'player'], keep=False)
    # df_dup = df_merged[dup_mask]

    # # 找出在這些重複中，"salary 是 NaN 且 age 有值" 的列
    # to_drop = df_dup[df_dup['salary'].isna() & df_dup['age'].notna()]

    # # 從原始 DataFrame 移除這些列
    # df_cleaned = df_merged.drop(index=to_drop.index)

    
    df_merged.to_csv(f'output/nba_player_merge.csv', index=False, encoding="utf-8-sig")
    
    df = df_merged.copy()
    df = df.where(pd.notnull(df), None)

    data = df.to_dict(orient='records')

    # 確保所有 nan 都變成 None
    for row in data:
        for k, v in row.items():
            if isinstance(v, float) and pd.isna(v):
                row[k] = None 
    
    upload_data_to_mysql_upsert(nba_player_table, data)

