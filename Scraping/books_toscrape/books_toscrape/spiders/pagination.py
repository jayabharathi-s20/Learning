import scrapy
from ..items import PaginationItem
import re
import json

class PaginationSpider(scrapy.Spider):
    name = "pagination"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html",
                  "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
                  ]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
           
            relative_url= book.css("h3 a::attr(href)").get()
            # book_url='https://books.toscrape.com/catalogue/'+relative_url
            book_url=response.urljoin(relative_url)
            yield scrapy.Request(book_url,callback=self.parse_pagination,meta={"book_url":book_url,"pagination_url":response.url})

            next_page=response.css("li.next a::attr(href)").get()
        if next_page:    
            next_page_url=response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)

    def parse_pagination(self, response):

        # product_info = {
        #     k: v
        #     for k, v in zip(
        #         response.css("table.table-striped th::text").getall(),
        #         response.css("table.table-striped td::text").getall()
        #     )
        # }
        product_information = {}

        for row in response.css("table.table-striped tr"):
            key = row.css("th::text").get()
            value = row.css("td::text").get()

            if key and value:
                product_information[key.strip()] = [value.strip()]
                # product_information[key.strip()] = value.strip()


        item = PaginationItem()

        # item["category"] = response.css(".side_categories ul li:nth-child(3) a::text").get().strip()
        item["category"] = response.css("ul.breadcrumb li:nth-child(3) a::text").get().strip()
        item["title"] = response.css("h1::text").get()
        item["price"] = response.css(".price_color::text").get()
        item["description"] = response.css("#product_description ~ p::text").get()        
        item["image_url"] = response.urljoin(response.css(".item img::attr(src)").get())
        stock = response.css(".instock.availability").xpath("normalize-space()").get()
        item["stock"]=re.search(r"\((.*?)\)",stock).group(1)
        item["product_information"] = json.dumps(product_information, ensure_ascii=False)
        item["host_url"] = response.meta.get("book_url")
        item["pagination_url"] = response.meta.get("pagination_url")

        yield item
        
        

        

