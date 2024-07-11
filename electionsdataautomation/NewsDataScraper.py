import os
from datetime import datetime
from datetime import date

from gnews import GNews
import google.generativeai as genai
import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from tqdm.auto import tqdm
tqdm.pandas()

from KeywordFilter import KeywordFilter
from NewsArticle import NewsArticle


class NewsDataScraper:
    def __init__(self, base, api_key):
        self.getter = GNews(
            language='en', 
            country='CA', 
            start_date=date(2024, 6, 1),
            end_date=date.today())
        
        self.engine:Engine = create_engine(f"sqlite:///NewsArticles.db", echo=True)
        base.metadata.create_all(self.engine)
        self.filter: KeywordFilter = KeywordFilter()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                           safety_settings={
                                            'HATE': 'BLOCK_NONE',
                                            'HARASSMENT': 'BLOCK_NONE',
                                            'DANGEROUS': 'BLOCK_NONE'
                                            }
                                           )

    def get_articles(self, query):

        articles = self.getter.get_news(query)

        return articles

    def get_filtered_articles(self):
        topic_list = []
        articles = []

        for person in self.filter.people:
            topic_list.append(f"British Columbia AND {person}")
        hashes = []
        for query in tqdm(topic_list):
            temp = self.get_articles(query)
            for article in temp:
                desc_hash = hash((article['description'], article['published date'], article['publisher']['href']))
                # to_include = self.article_includes_transportation(article)
                to_include = True
                if desc_hash not in hashes and to_include:
                    articles.append(article)
                    hashes.append(desc_hash)
                else:
                    continue

        return articles


    def filter_articles(self, article):
        if article.text is None:
            return ''
        response = self.model.generate_content(
            f"""
            Please indicate whether or not the following aricle is related to 
            BC Government Transportation and Infrastructure Initiatives. Please
            respond with yes or no followed by an explanation.
            
            {article.text} 
            
            """
        )
        return response.text


    def summary_extraction(self, article):
        if article is None:
            return ''

        response = self.model.generate_content(
            f'''
            Please summarize the following article text:
            
            {article.text}
            ''',
        )
        try:
            return response.text
        except:
            print('pause')

    def article_includes_transportation(self, article):
        article_text = self.getter.get_full_article(article['url'])
        if article_text is None:
            return False
        keywords = self.filter.extractor.extract_keywords(article_text.text)
        keywords = set([keyword[0].lower() for keyword in keywords])
        people = self.filter.people
        people = [person.lower() for person in people]

        first_pass = set.intersection(set(keywords), set(people))

        return len(first_pass) > 0

    def write_to_db(self):
        articles = self.get_filtered_articles()
        articles = [ NewsArticle(
            title=article['title'],
            description=article['description'],
            date=datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S %Z'),
            publisher_url=article['publisher']['href'],
            url=article['url']
        ) for article in articles]
        with Session(self.engine) as sess:
            sess.add_all(articles)
            sess.commit()

        articles = [article.__dict__ for article in articles]
        article_df = pd.DataFrame.from_records(articles)
        article_df.to_sql('articles', self.engine, if_exists='append', index=False)

    def write_to_file(self):
        if not os.path.exists('articles.xlsx'):
            articles = self.get_filtered_articles()
            articles = [
                {
                    'title': article['title'],
                    'description': article['description'],
                    'date': datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S %Z'),
                    'publisher_url': article['publisher']['href'],
                    'summary': self.summary_extraction(self.getter.get_full_article(article['url'])),
                    'url': article['url']
                }
                for article in articles
            ]
            article_df = pd.DataFrame.from_records(articles)
            article_df.to_excel('articles.xlsx', index=False)
            # article_df.to_sql('articles', self.engine, if_exists='append', index=False)
        else:
            article_df = pd.read_excel('articles.xlsx')
            #article_df['summary'] = article_df['url'].apply(lambda x:
            #                                                self.summary_extraction(self.getter.get_full_article(x)))
            article_df['filter'] = article_df['url'].progress_apply(
                lambda x: self.filter_articles(self.getter.get_full_article(x))
            )
            article_df.to_csv('articles.csv', index=False)

