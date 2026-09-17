from google import genai
import pandas as pd
import os
from dotenv import load_dotenv
import json


class ai_summarizer():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("LLM_MODEL")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompt_path = os.path.join(script_dir, 'prompts/gemini_prompt.md')
        self.output_path = os.path.join(script_dir, 'data/gemini_output.txt')

        self.prompt = open(self.prompt_path, mode='r', encoding='latin-1').read()

    def run_ai(self, news_df):
        print('[STARTED LLM INFERENCE]')
        client = genai.Client(api_key=self.api_key)

        self.response = client.interactions.create(
            model=self.model, 
            input=f"""
        {self.prompt}
        {news_df[['date', 'title', 'content']].to_string()}
        """
        )

        print('[FINISHED LLM INFERENCE]')
        return self.response.output_text
        
    def save_file(self, input):
        with open(self.output_path, "w", encoding='utf-8') as file: 
            file.write(input)

        print('[SAVED SUMMARY FILE]')

class json_validator():
    def __init__(self):
        pass

    @staticmethod
    def validate_ai_output(output):
        #TODO: improve validator to also check formats
        def validation_error():
            print('[INVALID AI GENERATED JSON]')
            return False

        try:
            ai_json = json.loads(output)   

            if not (ai_json['title'] and ai_json['introduction'] and ai_json['summary']['paragraphs']):
                validation_error()

            for i in ai_json['sections']:
                if i['topics'] and i['title']:
                    for j in i['topics']:
                        if not j['paragraphs']:
                            validation_error()    
                else:
                    validation_error()
                    
            return True  
        except:
            validation_error()


def run(news_df, max_attempts):
    summarizer = ai_summarizer()
    current_attempts = 0
    while current_attempts <= max_attempts:
        current_attempts += 1
        response = summarizer.run_ai(news_df)
        if json_validator().validate_ai_output(response):
            return response
        else:
            continue
    return False


