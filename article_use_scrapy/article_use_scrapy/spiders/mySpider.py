from article_use_scrapy.items import ArticleUseScrapyItem

from scrapy.selector import Selector

from scrapy.spiders import Spider

class MySpider(Spider):
    name="Baidu_know"
    allowed_domains =["baidu.com"]
    start_urls =[
        "https://zhidao.baidu.com/list?cid=110",
        "https://zhidao.baidu.com/list?cid=110102"
    ]

    def parse(self,response):
        sel = Selector(response)
        items=[]
        item=ArticleUseScrapyItem()
        title= sel.xpath('//div[@class="question-title"]/a/text()').extract()
        print("XXXX : "+str(len(title)))
        for i in title:
            items.append(i)

        item["TitleName"]=items

        return item    