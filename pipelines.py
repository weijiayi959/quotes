# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#项目管道，可以输出一些items
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    # 对数据的清洗工作
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit]+'...'
            return item
        else:
            return DropItemm('Missing Text!')


class MongoPipeline(object):
    # 用来保存到mongodb数据库的初始化信息
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri     
        self.mongo_db = mongo_db       


    #从settings里拿到MONGO数据库的配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # 在进行spider前的初始化操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)   # 连接数据库
        self.db = self.client[self.mongo_db]              # 创建项目

    def process_item(self, item, spider):
        name = self.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()








