# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):

    url =  scrapy.Field()
    id = scrapy.Field()
    tag = scrapy.Field()
    header = scrapy.Field()
    intro = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
