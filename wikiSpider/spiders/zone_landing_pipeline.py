# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikiSpider.util import clean_date, clean_body, remove_links, remove_spaces
import os
import json
from datetime import date

class LandingZonePipeline:
    def __init__(self) -> None:
        # information path to save
        self.items = []
        self.today = str(date.today())
        self.output_dir = '../data_lake/landing_zone'
        os.makedirs(self.output_dir, exist_ok=True)

        
    def process_item(self, item, spider):
        
        self.items.append(ItemAdapter(item).asdict())
        return item
    
    def close_spider(self, spider):
        path = os.path.join(self.output_dir, f'{spider.name}_{self.today}.json')
        with open(path, 'w') as f:
            json.dump(self.items, f, indent=2)

