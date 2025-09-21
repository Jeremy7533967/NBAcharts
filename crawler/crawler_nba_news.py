"""
Filename:    scawler_salary.py
Author:      Shin Yuan Huang
Created:     2025-09-14 
Description: NBA news from https://www.nba.com/
"""
#%% import
import urllib.request as req
import bs4 as bs
import pandas as pd
import time
from datetime import datetime, timezone
import random

from data_ingestion.mysql import upload_data_to_mysql_upsert, nba_news_table




#%%

url_base = 'https://www.nba.com/'


# 取得網頁內容
r = req.Request(url_base)
r.add_header('user-agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')

# 開啟網址並讀取html內容
resp = req.urlopen(r)
content = resp.read()
html = bs.BeautifulSoup(content,'html.parser')
# %%

Headline_list = html.find_all('a', {"class": "Anchor_anchor__cSc3P", "data-type": "headline"})

title = []
link = []
label = []

for i in Headline_list:

    title_text = i.text.strip()
    full_url = f"{url_base}{i.get('href')}"

    # 進入full_url取得文章分類
    r = req.Request(full_url)
    r.add_header('user-agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')
    resp = req.urlopen(r)
    content = resp.read()
    html = bs.BeautifulSoup(content,'html.parser')
    label_text = html.find('h3', class_='ArticleHeader_ahCattext__ukmoa').text.strip()

    title.append(title_text)
    link.append(full_url)
    label.append(label_text)

    time.sleep(random.uniform(3, 5))  # 輕微延遲，避免封鎖

all_rows = []
for i in range(len(title)):
    all_rows.append({
        'datetime': datetime.now(timezone.utc).date(),
        'title': title[i],
        'label': label[i],
        'link': link[i],
        'uploaded_at': datetime.now(timezone.utc)
    })
df = pd.DataFrame(all_rows)



# %%
