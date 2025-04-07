# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikiSpider.util import clean_date, clean_body
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class RefinedDbPipeline:
    def __init__(self) -> None:
        # information Connection with db
        hostname = os.getenv('DB_HOST')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')

        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
            )
        print("***")
        print("Conection to DB successful.....")
        self.connection.set_client_encoding('UTF8')
        self.cur = self.connection.cursor()

        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS news(
                         id TEXT PRIMARY KEY,
                         url TEXT,
                         tag TEXT,
                         header TEXT,
                         intro TEXT,
                         date TEXT,
                         body TEXT
                         )                        
                        """)
        self.connection.commit()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        self.cur.execute("""
                        SELECT * FROM news WHERE id = %s""", (adapter['id'],))

        res = self.cur.fetchone()

        if res:
            print(f"This item: {adapter['id']} is already in the DB")
            spider.logger.info("The item is already in the DB, skipping.")
        else:
            self.cur.execute("""
                        INSERT INTO news (id, url, tag, header, intro, date, body)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                            adapter['id'],
                            adapter['url'],
                            adapter['tag'],
                            adapter['header'],
                            adapter['intro'],
                            adapter['date'],
                            adapter['body']
                            ) 
                        )
            self.connection.commit()
        
        return item
    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()