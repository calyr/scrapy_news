# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikiSpider.util import clean_date, clean_body, convert_timestamps, fix_encoding_issues, decode_text, remove_links, remove_spaces
import os
import json
from datetime import date

class RefinedZonePipeline:
    def __init__(self) -> None:
        # information path to save
        self.items = []
        self.today = str(date.today())
        self.output_dir = 'wikiSpider/data_lake/refined_zone'
        os.makedirs(self.output_dir, exist_ok=True)


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
                tmp_val = adapter.get(field)
                tmp_val = fix_encoding_issues(tmp_val)
                tmp_val = decode_text(tmp_val)
                adapter[field] = tmp_val
            if field == 'body':
                tag_value = adapter.get(field)
                # print(f"body_value {tag_value}")
                tmp_val = clean_body(tag_value)
                tmp_val = remove_links(tmp_val)
                tmp_val = remove_spaces(tmp_val)
                tmp_val = fix_encoding_issues(tmp_val)
                tmp_val = decode_text(tmp_val)
                adapter[field] = tmp_val    

        self.items.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        path = os.path.join(self.output_dir, f'{spider.name}_{self.today}.json')
        with open(path, 'w') as f:
            json.dump(convert_timestamps(self.items), f, indent=2, ensure_ascii=False)