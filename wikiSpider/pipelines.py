# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikiSpider.util import clean_date, clean_body

class WikispiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        print("***********")
        for field in fields:
            print(f'Item {field}')
            if field == 'tag':
                tag_value = adapter.get(field)
                print(f"tag_value {tag_value}")
                tmp_val = tag_value.upper()
                adapter[field] = tmp_val
            if field == 'date':
                date_value = adapter.get(field)
                tmp_val = clean_date(date_value)
                adapter[field] = tmp_val
            if field == 'id':
                tag_value = adapter.get(field)
                print(f"id_value {tag_value}")
                tmp_val = tag_value
                adapter[field] = tmp_val
            if field == 'intro':
                tag_value = adapter.get(field)
                print(f"intro_value {tag_value}")
                tmp_val = tag_value.strip()
                adapter[field] = tmp_val
            if field == 'header':
                tag_value = adapter.get(field)
                print(f"header_value {tag_value}")
                tmp_val = tag_value.lower()
                adapter[field] = tmp_val
            if field == 'body':
                tag_value = adapter.get(field)
                print(f"body_value {tag_value}")
                tmp_val = clean_body(tag_value)
                adapter[field] = tmp_val
        return item