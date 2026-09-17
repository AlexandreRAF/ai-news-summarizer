import json
from pathlib import Path
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

class news_json_generator():
    def __init__(self):
        load_dotenv()
        self.model = os.getenv("LLM_MODEL")
        self.current_dir = Path(__file__).resolve().parent
        self.settings = json.load(open('%s/settings.jsonc' % self.current_dir, "r"))

    def finish_json(self, ai_output, news_df):
        json_object = json.loads(ai_output)

        json_object['language'] = self.settings['document_presets']['language']
        json_object['publication'] = self.settings['document_presets']['publication']
        json_object['category'] = self.settings['document_presets']['category']

        json_object['metadata'] = {}
        json_object['metadata']['period'] = {}
        json_object['metadata']['period']['start'] = news_df['date'].min().isoformat()
        json_object['metadata']['period']['end'] = news_df['date'].max().isoformat()
        json_object['metadata']['generatedAt'] = datetime.now().astimezone().isoformat()
        json_object['metadata']['model'] = self.model

        json_object['sources'] = {}
        json_object['sources']['items'] = self.create_sources_array(news_df)

        json_object['footer'] = {}
        json_object['footer']['paragraphs'] = self.settings['document_presets']['footer_text']

        return json_object

    @staticmethod
    def create_sources_array(news_df):
        items = []
        for i in range(len(news_df)):
            title = news_df.iloc[i]['title']
            date = news_df.iloc[i]['date'].isoformat()
            url = news_df.iloc[i]['link']

            items.append({"title": title, "publishedAt": date, "url": url})
        return items

    def write_json(self, json_content):
        with open("%s/pdf_generator/temp/news.json" % self.current_dir, "w") as file:
            file.write(json_content)

def run(ai_output, news_df):
    generator = news_json_generator()
    updated_json = generator.finish_json(ai_output, news_df)
    generator.write_json(str(json.dumps(updated_json)))

news_json_generator()

