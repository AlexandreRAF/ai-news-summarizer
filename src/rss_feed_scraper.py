import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
from pathlib import Path
from email.utils import parsedate_to_datetime


class rss_scraper():
    def __init__(self):
        CURRENT_DIR = Path(__file__).resolve().parent
        cfg_file = json.load(open('%s/feeds.jsonc' % CURRENT_DIR, "r"))
        self.feeds = cfg_file['feeds']
        self.newsDF = pd.DataFrame()
        
    def scrape_rss_feed(self):
        for feed in self.feeds:
            try:
                xml_data = requests.get(feed, headers={"User-Agent": "Mozilla/5.0"}).content
            except Exception as e:
                print('[ERROR LOADING RSS FEED][%s]' % feed, e)
                continue

            soup = BeautifulSoup(xml_data, "xml")

            dates = []
            titles = []
            contents = []
            links = []

            for item in soup.find_all('item'):
                date = item.find('pubDate').text.strip()
                title = item.find('title').text.strip()
                link = item.find('link').text.strip()
                html_content = item.find('description').text

                clean_text = BeautifulSoup(html_content, "html.parser").get_text(" ", strip=True)

                dates.append(date)
                titles.append(title)
                contents.append(clean_text)
                links.append(link)

            df = pd.DataFrame({'date' : dates, 'title' : titles, 'content' : contents, 'link' : links})
            df['date'] = pd.to_datetime(df['date'].map(parsedate_to_datetime), utc=True)

            self.newsDF = pd.concat([self.newsDF, df], ignore_index=True)

        return True

    def filter_df(self, starting_date):
        if starting_date:
            date_start = pd.Timestamp(starting_date, tz='UTC')
            self.newsDF = self.newsDF[self.newsDF['date'] >= date_start].reset_index(drop=True)
            return self.newsDF
        else:
            return self.newsDF

def return_news_df(starting_date):
    try:
        scraper = rss_scraper()
        get_feed_data = scraper.scrape_rss_feed()
        if get_feed_data:
            return scraper.filter_df(starting_date)
        else:
            print('[ERROR EXTRACTING DATA FROM RSS FEEDS]')
            return False
    except Exception as e:
        print('[ERROR EXTRACTING DATA FROM RSS FEEDS]', e)
        return False

    
