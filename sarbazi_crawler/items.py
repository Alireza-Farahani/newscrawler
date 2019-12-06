# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SarbaziCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# TODO: use pipeline for concatenation of 'text' paragraphs. (hmm, different class per news website?)
class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()            # optional
    date = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    source_article_url = scrapy.Field()  # optional
    summary = scrapy.Field()
    text = scrapy.Field()
