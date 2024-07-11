from electionsdataautomation.NewsDataScraper import NewsDataScraper
from electionsdataautomation.NewsArticle import Base
import dotenv
import os

dotenv.load_dotenv()

if __name__ == '__main__':

    scraper = NewsDataScraper(Base, os.environ['GOOGLE_GEMINI_API_KEY'])
    articles = scraper.write_to_file()
    