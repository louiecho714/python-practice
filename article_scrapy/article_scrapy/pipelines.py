# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from datetime import datetime
import re


class ArticleScrapyPipeline:
    collection_name = 'articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')#my_test_data
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        category=re.findall(r">\s[\u4e00-\u9fa5]+\s",item["category"][0])[0]
        category=category.replace("> ", "").replace(" ", "").replace("\n", "")

        data={
            "url":item["url"][0],
            "content":item["content"][0],
            "author":item["author"][0],
            "date":item["date"][0],
            "title":item["title"][0],
            "date":item["date"][0],
            "publishDate":datetime.strptime(item["publishDate"][0], "%Y-%m-%d"),
            "project":item["project"][0],
            "spider":item["spider"][0],
            "server":item["server"][0],
            "date":item["date"][0],
            "status":"NEW",
            "originalCategory":category,
            }
        
        self.db[self.collection_name].insert(data)

        return item
