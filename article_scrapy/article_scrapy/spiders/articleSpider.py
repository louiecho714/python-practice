import datetime
import urllib.parse as urllib_parse
import socket


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Join
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

         soup=BeautifulSoup(response.text,"html.parser")

        titleDiv = soup.find('div',class_="entry-header")

        content = soup.find("meta", property="og:description")   

        dateAndAuthor = titleDiv.find("p")

        matchDate = re.search(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))',dateAndAuthor.text)

        index = dateAndAuthor.text.find(":")
        author= dateAndAuthor.text[index+1:].strip()

        return {
            "url":articleUrl,
            "title":titleDiv.h1.text,
            "author":author,
            "publishDate":matchDate.group(1),
            "content":content["content"],

        # Create the loader using the response
        l = ItemLoader(item=ArticleScrapyItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('title', '//div[@class="entry-header"]/h1/text()',
                    MapCompose(str.strip))
        l.add_xpath('content', '//meta[@property="og:description"]/@content',
                    MapCompose(str.strip))
        l.add_value('url',response.url)
        l.add_xpath('author',
                    '//div[@class="entry-header"]/p[1]/text()[2]',
                    MapCompose(lambda i: i.replace(',', ''), float))
        l.add_xpath('publishDate', '//div[@class="entry-header"]/p[1]/text()[1]',
                    MapCompose(lambda i: urllib_parse.urljoin(response.url, i)))

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
