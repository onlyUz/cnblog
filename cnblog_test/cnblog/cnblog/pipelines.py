# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class CnblogPipeline:
    def __init__(self, sql_host, sql_port, sql_name, sql_set):
        self.client = None
        self.collection = None
        self.sql_host = sql_host
        self.sql_port = sql_port
        self.sql_name = sql_name
        self.sql_set = sql_set

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            sql_host=settings.get('SQL_HOST'),
            sql_port=settings.get('SQL_PORT'),
            sql_name=settings.get('SQL_NAME'),
            sql_set=settings.get('SQL_SET')
        )

    def open_spider(self, spider):
        print('----开始爬虫---')
        self.client = pymongo.MongoClient(host=self.sql_host, port=int(self.sql_port))
        db = self.client[self.sql_name]
        self.collection = db[self.sql_set]

    def close_spider(self, spider):
        print('---结束爬虫---')
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
