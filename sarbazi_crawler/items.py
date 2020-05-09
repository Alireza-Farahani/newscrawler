# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join
from w3lib.html import remove_tags, remove_tags_with_content

# TODO: base item, having an id to be checked in DuplicatePipeline. For example 'url' could be id for Articles
# class BaseItem(scrapy.Item)
# class Article(BaseItem)
from sarbazi_crawler.utils import DropLast, Replace, remove_unicode_whitespaces


class ArticleItem(scrapy.Item):
    url = scrapy.Field()  # all sites
    title = scrapy.Field()  # all sites
    subtitle = scrapy.Field()  # sciencedaily, livescience
    author = scrapy.Field()
    date = scrapy.Field()  # all
    source = scrapy.Field()  # optional in sciencedaily, sciencealert
    source_article_url = scrapy.Field()  # optional in sciencedaily, sciencealert TODO:
    summary = scrapy.Field()  # sciencedaily
    content = scrapy.Field()  # all
    # category = scrapy.Field  # all TODO: how to know the category? only sciencealert has it per article


class ArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_tags, str.strip)
    url_in = Identity()


class LiveScienceArticleLoader(ArticleLoader):
    # Fixme: what to do with 'Update on data' lines?
    # returning None drops that scraped item. see https://docs.scrapy.org/en/latest/topics/loaders.html
    content_in = Compose(
        MapCompose(lambda x: None if "<strong>Related" in x else x,  # related posts
                   lambda x: None if "<em>[" in x else x,  # signup for source newsletter
                   lambda x: None if "<strong>Read more:" in x else x,  # related post
                   remove_unicode_whitespaces,
                   ArticleLoader.default_input_processor,
                   lambda x: None if x == '' else x, ),  # there are some empty paragraphs
        DropLast(),  # last p not related to article body (mostly 'Originally published in LIVESCIENCE')
        Join('\n\n'), )

    date_out = Compose(
        TakeFirst(),
        lambda iso_date: iso_date.replace("Z", "+00:00"),  # https://stackoverflow.com/q/19654578/1660013
        lambda iso_date: datetime.fromisoformat(iso_date).date(), )


class ScienceAlertLoader(ArticleLoader):
    # FIXME: not sure about removing <span> with content. is it only used when putting image in content?
    content_in = Compose(
        MapCompose(lambda x: remove_tags_with_content(x, 'div', 'span'),
                   lambda x: None if x.startswith("<p><em><a") else x,  # authors info. possible FalsePositive?
                   remove_unicode_whitespaces,
                   ArticleLoader.default_input_processor),
        DropLast(),  # last p is about source article
        Join('\n\n'), )

    author_in = MapCompose(
        ArticleLoader.default_input_processor,
        lambda author_str: author_str[:author_str.index(',')] if ',' in author_str else author_str,
        str.title  # 'WILLIAM PORTER' to 'William Porter'
    )

    date_out = Compose(  # sciencealert format: 3 FEBRUARY 2020
        TakeFirst(),
        lambda date_str: datetime.strptime(date_str, "%d %B %Y").date(), )


class ScienceDailyArticleLoader(ArticleLoader):
    content_in = Compose(
        Join('\n\n'),
        lambda x: remove_tags_with_content(x, ('div',)),  # there's "div"s for advertisements
        ArticleLoader.default_input_processor,
    )

    date_out = Compose(
        TakeFirst(),
        lambda date_str: datetime.strptime(date_str, "%B %d, %Y").date(), )


class ScienceNewsLoader(ArticleLoader):
    content_in = Compose(
        MapCompose(
            Replace("\n", " "),  # sometimes SN inserts new line instead of space. Extra space is better than new line.
            ArticleLoader.default_input_processor
        ),
        Join('\n\n'),
    )

    date_out = Compose(
        TakeFirst(),
        lambda iso_date: datetime.fromisoformat(iso_date).date(),
    )


class ScientificAmericanLoader(ArticleLoader):
    content_in = Compose(
        MapCompose(
            ArticleLoader.default_input_processor,
            lambda x: None if x == '' else x,  # there are some empty paragraphs,
            lambda x: None if 'Read more about' in x else x,  # drop link to other sources
        ),
        Join('\n\n'),
    )

    author_in = MapCompose(
        ArticleLoader.default_input_processor,
        lambda author_str: author_str[:author_str.index(',')] if ',' in author_str else author_str
    )

    date_out = Compose(
        TakeFirst(),
        lambda date_str: datetime.strptime(date_str, "%B %d, %Y").date()
    )
