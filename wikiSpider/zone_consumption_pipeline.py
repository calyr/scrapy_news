# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from wikiSpider.util import convert_timestamps
from datetime import date
import pandas as pd


class ConsumptionPipeline:
    def __init__(self) -> None:
        # information path to save
        self.items = []
        self.today = str(date.today())
        self.output_dir = 'wikiSpider/data_lake/consumption_zone'
        os.makedirs(self.output_dir, exist_ok=True)


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.items.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        print("Total items recolectados:", len(self.items))  # Verifica cuántos elementos tienes
        if self.items:
            # Guardar también como CSV
            csv_path = os.path.join(self.output_dir, f'{spider.name}_{self.today}.csv')
            print(f"Guardando archivo CSV en: {csv_path}")  # Asegúrate de que esta ruta es correcta
            df = pd.DataFrame(convert_timestamps(self.items))
            df.to_csv(csv_path, index=False)
        else:
            print("No se encontraron items para guardar en CSV")