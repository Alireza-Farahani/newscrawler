# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join
from w3lib.html import remove_tags, remove_tags_with_content


class SarbaziCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# TODO: base item, having an id to be checked in DuplicatePipeline. For example 'url' could be id for Articles
# class BaseItem(scrapy.Item)
# class Article(BaseItem)


# TODO: different class per news website?
class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()  # optional
    date = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    source_article_url = scrapy.Field()  # optional
    summary = scrapy.Field()
    text = scrapy.Field()


class ArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_tags, str.strip)

    url_in = Identity()
    text_in = Compose(Join(),
                      lambda x: remove_tags_with_content(x, ('div',)),  # there's "div"s for advertisements
                      remove_tags,
                      str.strip)

