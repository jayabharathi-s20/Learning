import scrapy
from ..items import QuoteTutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):

        all_div_quotes = response.css("div.quote")

        for quote in all_div_quotes:
            items = QuoteTutorialItem()

            title = quote.css('span.text::text').get()
            author = quote.css(".author::text").get()
            tags = quote.css(".tag::text").getall()

            if title:
                title = title.replace("“", "").replace("”", "").strip()

            items["title"] = title
            items["author"] = author
            items["tags"] = tags

            yield items