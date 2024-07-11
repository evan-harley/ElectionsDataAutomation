from electionsdataautomation.NewsDataScraper import NewsDataScraper
from electionsdataautomation.NewsArticle import Base

if __name__ == '__main__':

    scraper = NewsDataScraper(Base)
    articles = scraper.write_to_file()
    