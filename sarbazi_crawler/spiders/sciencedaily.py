from itertools import chain

from scrapy import Spider
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import ArticleItem, ScienceDailyArticleLoader


class ScienceDailySpider(Spider):
    name = 'sciencedaily'
    allowed_domains = ['sciencedaily.com']
    start_urls = [
        'https://www.sciencedaily.com/news/matter_energy/',
        'https://www.sciencedaily.com/news/computers_math/',
        'https://www.sciencedaily.com/news/space_time/',
    ]

    def parse(self, response):
        # In Sciencedaily category pages, news link are separated in 3 segment:
        # top headlines, latest headlines and earlier headlines. We need all of them to ensure we don't miss anything.

        # scrapy docs says use css selectors when selecting by tag/elements's class
        # https://docs.scrapy.org/en/latest/topics/selectors.html#when-querying-by-class-consider-using-css
        top_headlines = response.css('div#heroes h3.latest-head a')
        latest_headlines = response.css('ul#featured_shorts a')
        earlier_headlines_segment = response.css('div#headlines')
        earlier_headlines = earlier_headlines_segment.css('ul > li > a')
        for link in chain(top_headlines, latest_headlines, earlier_headlines):
            yield response.follow(link, callback=self.parse_news)

        # TODO: another way could be iterate on news_by_dates, see if there are news for 'today' and just add them.
        # this is independent of 'Job' but for robustness we need to check links against database, add them until the
        # first duplicate link.
        # news_by_dates = earlier_headlines_segment.xpath("./child::*")  # all tag/element children

    # noinspection PyMethodMayBeStatic
    def parse_news(self, response):
        loader: ItemLoader = ScienceDailyArticleLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        loader.add_css('title', 'h1#headline')
        loader.add_css('subtitle', 'h2#subtitle')  # optional

        loader.add_css('date', 'dd#date_posted')  #
        loader.add_css('source', 'dd#source')  #

        loader.add_css('content', 'div#text > p')  # <p>s are joined in related 'Item Loader'

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        # see nesting loaders https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders
        source_segment_loader = loader.nested_css('div#story_source > p:nth-child(2)')
        source_segment_loader.add_xpath('source_article_url', "./a[contains(text(), 'Materials')]/@href")  # optional

        yield loader.load_item()
