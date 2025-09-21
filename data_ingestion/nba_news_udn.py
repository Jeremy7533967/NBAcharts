import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from data_ingestion.mysql import upload_data_to_mysql_upsert, nba_news_udn_table
from data_ingestion.nba_common import convert_date  # 引入共用的日期轉換函數



def nba_news_udn():
    all_articles = []
    base_url = 'https://tw-nba.udn.com/api/more?channel_id=2000&type=index&page='
    page_num = 1

    while True:
        url = f"{base_url}{page_num}"
        news = requests.get(url)

        if news.status_code == 200:
            soup = BeautifulSoup(news.text, 'html.parser')
            articles_on_page = []
            for dt in soup.find_all('dt'):
                link = dt.find('a')
                if link:
                    url = link.get('href')
                    title = link.find('h3').text if link.find('h3') else 'N/A'
                    date = link.find('b', class_='h24').text if link.find('b', class_='h24') else 'N/A'
                    articles_on_page.append({'title': title, 'url': url, 'date': date})

            if not articles_on_page:
                # No articles found on this page, so we've reached the end
                print(f"No articles found on page {page_num}. Stopping.")
                break
            else:
                all_articles.extend(articles_on_page)
                print(f"Successfully retrieved {len(articles_on_page)} articles from page {page_num}")
                page_num += 1
        else:
            print(f"Failed to retrieve data from page {page_num}. Status code: {news.status_code}. Stopping.")
            break

    news_df = pd.DataFrame(all_articles)

    # 對每一個日期值進行轉換
    news_df['date'] = news_df['date'].apply(convert_date)

    # 確保日期欄位是字串格式 YYYY-MM-DD
    news_df['date'] = news_df['date'].astype(str)
    #建立ID
    news_df['id'] = news_df['url'].apply(lambda x: x.split('/')[-1].replace('.html', ''))

    dirname = "nba_news"
    if not os.path.exists(dirname):
            os.mkdir(dirname)
            
    news_df.to_csv(f'{dirname}/nba_news_udn.csv', index=False, encoding='utf-8-sig', escapechar='\\')
    print(f"Total articles retrieved: {len(news_df)}")

    data = news_df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(table_obj=nba_news_udn_table, data=data)
    print(f"nba_news_udn has been upsert to mysql.")

if __name__ == '__main__':
    nba_news_udn()