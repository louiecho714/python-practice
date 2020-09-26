import datetime
import urllib.parse as urllib_parse
import socket


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Join,TakeFirst
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader


from article_scrapy.items import ArticleScrapyItem


class ArticlespiderSpider(CrawlSpider):
    name = 'articleSpider'
    allowed_domains = ['www.wealth.com.tw']
    start_urls = ['http://www.wealth.com.tw/']

    # Rules for horizontal and vertical crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="dropdown-menu"]/li/a[starts-with(@href, "/home/articles?category_id=")]')),
        Rule(LinkExtractor(restrict_xpaths='//ul/li//a[@rel="next"]/i/..')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="posts-group"]/article/a'),
             callback='parse_item')
    )

    def parse_item(self, response):

        # Create the loader using the response
        l = ItemLoader(item=ArticleScrapyItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        l.add_xpath('content', '//meta[@property="og:description"]/@content')
        l.add_xpath('author','//div[@class="entry-header"]/p[1]/text()[2]',MapCompose(lambda i: i.replace('作者: ', '')))

        l.add_xpath('publishDate', '//div[@class="entry-header"]/p[1]/text()[1]')

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
