from scrapy import Spider
from scrapy.http import Response, TextResponse
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import ArticleItem, ScienceAlertLoader


class ScienceDailySpider(Spider):
    name = 'sciencealert'
    allowed_domains = ['sciencealert.com']
    start_urls = [
        'https://www.sciencealert.com/health',
        'https://www.sciencealert.com/tech',
        'https://www.sciencealert.com/physics',
    ]

    def parse(self, response: Response):
        # In Sciencedaily category pages, news link are separated in 3 segment:
        # top headlines, latest headlines and earlier headlines. We need all of them to ensure we don't miss anything.

        # scrapy docs says use css selectors when selecting by tag/elements's class
        # https://docs.scrapy.org/en/latest/topics/selectors.html#when-querying-by-class-consider-using-css
        latest_news = response.css("div#rt-mainbody div.latestnews div.titletext a")
        for link in latest_news:
            yield response.follow(link, callback=self.parse_news)

    # noinspection PyMethodMayBeStatic
    def parse_news(self, response: TextResponse):
        loader: ItemLoader = ScienceAlertLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        # see nesting loaders https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders
        article_loader = loader.nested_css("div.main-article")
        article_loader.add_css('title', "h1")

        # TODO: some articles have date in div.author-name-name! e.g.
        # https://www.sciencealert.com/us-life-expectancy-just-increased-for-the-first-time-in-4-years
        # So in these cases we pick second 'author-name-name'
        if len(response.css("div.author-name-date span")) == 1:
            css_sel = "div.author-name-date span"
        else:
            css_sel = "div.author-name-name:last-child span"
        article_loader.add_css('date', css_sel)

        body_loader = article_loader.nested_css("div.article-fulltext")
        body_loader.add_css('content', "p")  # <p>s are joined in related 'Item Loader'

        # TODO: filter source and source_article
        # example hard url: https://www.sciencealert.com/scientists-have-built-robots-entirely-out-of-living-frog-cells
        # body_loader.add_xpath('p[last()]')

        yield loader.load_item()
