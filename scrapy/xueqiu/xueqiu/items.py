# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XueqiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    current_price = scrapy.Field()
    percent = scrapy.Field()
