# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ArticleUseScrapyPipeline:
    def process_item(self, item, spider):
        file = open('/Users/louie/python-practice/data.txt','a')
        for i in item['TitleName']:
            value = i.replace('\n',"")
            file.write(value+"\r\n")
        file.close()    
        return item
