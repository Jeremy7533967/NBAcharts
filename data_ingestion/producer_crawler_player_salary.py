from data_ingestion.tasks_crawler_player_salary import player_year_salary

years = list(range(2015,2026))

for year in years:
    player_year_salary.delay(year)