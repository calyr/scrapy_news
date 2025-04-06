# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def select_data(value):
    if isinstance(value, tuple) and len(value) > 0:
        return value[0]
    return value

class NewsItem(scrapy.Item):

    url =  scrapy.Field(serializer=select_data)
    id = scrapy.Field(serializer=select_data)
    tag = scrapy.Field(serializer=select_data)
    header = scrapy.Field(serializer=select_data)
    intro = scrapy.Field(serializer=select_data)
    date = scrapy.Field(serializer=select_data)
    body = scrapy.Field(serializer=select_data)

    def __getitem__(self, key):
        """
        Override __get__ to apply serializers when accessing fields
        This ensures serializers are applied during item access
        """
        value = super(NewsItem, self).__getitem__(key)
        field = self.fields[key]
        if 'serializer' in field:
            return field['serializer'](value)
        return value

