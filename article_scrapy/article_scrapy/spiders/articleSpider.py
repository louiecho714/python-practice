import scrapy


class ArticlespiderSpider(scrapy.Spider):
    name = 'articleSpider'
    allowed_domains = ['www.wealth.com.tw']
    start_urls = ['http://www.wealth.com.tw/']

    def parse(self, response):
        pass
