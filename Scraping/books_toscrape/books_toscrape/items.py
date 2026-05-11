# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksToscrapeItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    title_link = scrapy.Field()
       

