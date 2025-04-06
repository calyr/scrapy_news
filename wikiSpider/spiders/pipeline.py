# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikiSpider.util import clean_date, clean_body, remove_links, remove_spaces
import psycopg2
from dotenv import load_dotenv
import os
import re
load_dotenv()

class WikispiderPipeline:
    # def __init__(self) -> None:
        # # information Connection with db
        # hostname = os.getenv('DB_HOST')
        # username = os.getenv('DB_USER')
        # password = os.getenv('DB_PASSWORD')
        # database = os.getenv('DB_DATABASE')

        # self.connection = psycopg2.connect(
        #     host=hostname,
        #     user=username,
        #     password=password,
        #     dbname=database
        #     )
        # print("***")
        # print("Conection to DB successful.....")

        # self.cur = self.connection.cursor()

        # self.cur.execute("""
        #                 CREATE TABLE IF NOT EXISTS news(
        #                  id TEXT PRIMARY KEY,
        #                  url TEXT,
        #                  tag TEXT,
        #                  header TEXT,
        #                  intro TEXT,
        #                  date TEXT,
        #                  body TEXT
        #                  )                        
        #                 """)
        # self.connection.commit()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        for field in fields:
            # print(f'Item {field}')
            if field == 'tag':
                tag_value = adapter.get(field)
                # print(f"tag_value {tag_value}")
                tmp_val = tag_value.upper()
                adapter[field] = tmp_val
            if field == 'date':
                date_value = adapter.get(field)
                tmp_val = clean_date(date_value)
                adapter[field] = tmp_val
            if field == 'id':
                tag_value = adapter.get(field)
                # print(f"id_value {tag_value}")
                tmp_val = tag_value
                adapter[field] = tmp_val
            if field == 'intro':
                tag_value = adapter.get(field)
                # print(f"intro_value {tag_value}")
                tmp_val = tag_value.strip()
                adapter[field] = tmp_val
            if field == 'header':
                tag_value = adapter.get(field)
                # print(f"header_value {tag_value}")
                tmp_val = tag_value.lower()
                adapter[field] = tmp_val
            if field == 'body':
                tag_value = adapter.get(field)
                # print(f"body_value {tag_value}")
                tmp_val = clean_body(tag_value)
                tmp_val = remove_links(tmp_val)
                tmp_val = remove_spaces(tmp_val)
                adapter[field] = tmp_val
        
        # self.cur.execute("""
        #                 SELECT * FROM news WHERE id = %s""", (adapter['id'],))

        # res = self.cur.fetchone()

        # if res:
        #     print(f"This item: {adapter['id']} is already in the DB")
        #     raise Exception("The item is already in the DB")
        # else:
        #     self.cur.execute("""
        #                 INSERT INTO news (id, url, tag, header, intro, date, body)
        #                 VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
        #                     adapter['id'],
        #                     adapter['url'],
        #                     adapter['tag'],
        #                     adapter['header'],
        #                     adapter['intro'],
        #                     adapter['date'],
        #                     adapter['body']
        #                     ) 
        #                 )
        #     self.connection.commit()
        
        return item
    # def close_spider(self, spider):
    #     if self.cur:
    #         self.cur.close()
    #     if self.connection:
    #         self.connection.close()

