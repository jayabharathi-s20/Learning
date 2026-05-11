import scrapy
from ..items import BooksToscrapeItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css("article.product_pod")
        for book in books:
            items=BooksToscrapeItem()

            title=book.css("h3 a::attr(title)").get()
            price=book.css(".price_color::text").get()
            title_link=book.css("h3 a::attr(href)").get()

           
            items["title"]=title
            items["price"]=price
            items["title_link"]=title_link

            yield items
            
