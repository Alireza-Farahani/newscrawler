# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy import Item
from scrapy.exceptions import DropItem


class SarbaziCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


# TODO: This should only be triggered for article items. how?
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item: Item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item.get('url', item))
        else:
            self.ids_seen.add(item['url'])
            return item


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(  # TODO: correct name for db and collection
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            collection_name=crawler.settings.get('MONGO_COLLECTION', 'articles')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
