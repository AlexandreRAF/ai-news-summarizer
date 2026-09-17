import rss_feed_scraper
import llm
import json_generator
import pdf_generator.generator as pdf
import argparse
import sys

class initialize():
    def __init__(self):
        self.initialize_args()
        news_df = rss_feed_scraper.return_news_df(starting_date=self.date_start)
        ai_output = llm.run(news_df, 1)
        json_generator.run(ai_output, news_df)
        pdf.run(self.output_path)

    def initialize_args(self):
        # Set and parse the arguments 
        parser = argparse.ArgumentParser()
        
        parser.add_argument("-o", "--output-path", nargs=1, help="PDF file output path (include the file name and .pdf extension)", required=True)
        parser.add_argument("-s", "--start-date", nargs=1, help="Starting period to filter the news (YYYY-MM-DD)", required=False)

        args = parser.parse_args()

        self.output_path = args.output_path[0]
        self.date_start = False if not args.start_date else args.start_date[0]

def main():
    initialize()

if __name__ == "__main__":
    sys.exit(main())



        


