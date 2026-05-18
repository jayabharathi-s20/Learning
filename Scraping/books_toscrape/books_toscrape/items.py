# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BooksToscrapeItem(scrapy.Item):
    host_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    stock = scrapy.Field()
    product_information = scrapy.Field()

class PaginationItem(scrapy.Item):
    category = scrapy.Field()
    host_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    stock = scrapy.Field()
    product_information = scrapy.Field()
    pagination_url=scrapy.Field()
    created_at=scrapy.Field()
    updated_at=scrapy.Field()
    
    



       

