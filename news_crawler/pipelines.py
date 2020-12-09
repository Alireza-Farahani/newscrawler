# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date, timezone, datetime
from typing import Union

from pymongo import MongoClient
from scrapy import Item, Spider
from scrapy.exceptions import DropItem
from spidermon.contrib.scrapy.pipelines import ItemValidationPipeline


class CustomItemValidationPipeline(ItemValidationPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        parent = ItemValidationPipeline.from_crawler(crawler)
        return cls(parent.validators,
                   crawler.stats,
                   parent.drop_items_with_errors,
                   parent.add_errors_to_items,
                   parent.errors_field)

    def __init__(
            self,
            validators,
            stats,
            drop_items_with_errors,
            add_errors_to_items,
            errors_field=None,
    ):
        super().__init__(validators, stats, drop_items_with_errors, add_errors_to_items, errors_field)
        self.spider_name: str = "not specified"
        utc_dt = datetime.now(timezone.utc)  # UTC time
        self.tehran_time = utc_dt.astimezone()  # local time

    def open_spider(self, spider: Spider):
        self.spider_name = spider.name

    def _drop_item(self, item, errors):
        with open(f'{self.tehran_time.date()}-{self.spider_name}-errors.log', mode="a") as errors_file:
            item[self.errors_field]['url'] = item['url']
            errors_file.write(str(item[self.errors_field]) + "\n")

        super(CustomItemValidationPipeline, self)._drop_item(item, errors)


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

        self.client, self.db = None, None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(  # TODO: correct name for db
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'crawler'),
            collection_name=crawler.settings.get('MONGO_COLLECTION',
                                                 crawler.spider.name if crawler.spider else "temp_spider")
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
