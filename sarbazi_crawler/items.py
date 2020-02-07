# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import List

import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join
from w3lib.html import remove_tags, remove_tags_with_content


# TODO: base item, having an id to be checked in DuplicatePipeline. For example 'url' could be id for Articles
# class BaseItem(scrapy.Item)
# class Article(BaseItem)


def drop_last(values: List):  # could be changed to a processor class later.
    return values[:-1]


def remove_unicode_whitespaces(value: str):
    return value.replace('\xa0', '')


class ArticleItem(scrapy.Item):
    url = scrapy.Field()  # all sites
    title = scrapy.Field()  # all sites
    subtitle = scrapy.Field()  # sciencedaily, livescience
    date = scrapy.Field()  # all TODO: currently string, change processor to Date format in subclasses per site format
    source = scrapy.Field()  # optional in sciencedaily, sciencealert
    source_article_url = scrapy.Field()  # optional in sciencedaily, sciencealert TODO:
    summary = scrapy.Field()  # sciencedaily
    content = scrapy.Field()  # all
    # category = scrapy.Field  # all TODO: how to know the category? only sciencealert has it per article


class ArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_tags, str.strip)
    url_in = Identity()
    tags_out = Identity()


class ScienceDailyArticleLoader(ArticleLoader):
    content_in = Compose(Join(),
                         lambda x: remove_tags_with_content(x, ('div',)),  # there's "div"s for advertisements
                         remove_tags,
                         str.strip, )


class LiveScienceArticleLoader(ArticleLoader):
    # Fixme: what to do with 'Update on data' lines?
    # returning None drops that scraped item. see https://docs.scrapy.org/en/latest/topics/loaders.html
    content_in = Compose(MapCompose(lambda x: None if "<strong>Related" in x else x,  # related posts
                                    lambda x: None if "<em>[" in x else x,  # signup for source newsletter
                                    remove_tags,
                                    remove_unicode_whitespaces,
                                    str.strip),
                         drop_last,  # last p not related to article body (mostly 'Originally published in LIVESCIENCE)
                         Join(), )


class ScienceAlertLoader(ArticleLoader):
    # FIXME: not sure about removing <span> with content. is it only used when putting image in content?
    content_in = Compose(MapCompose(lambda x: remove_tags_with_content(x, 'div', 'span'),
                                    remove_tags,
                                    remove_unicode_whitespaces,
                                    str.strip),
                         drop_last,  # last p is about source article
                         Join(), )
