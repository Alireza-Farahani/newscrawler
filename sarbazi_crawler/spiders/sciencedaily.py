from scrapy import Spider
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import Article, ArticleLoader


# TODO: take account of 'latest-headlines' part! They aren't included in headlines segment
class ScienceDailySpider(Spider):
    name = 'science_daily'
    allowed_domains = ['sciencedaily.com']
    start_urls = [
        'https://www.sciencedaily.com/news/matter_energy/',
        'https://www.sciencedaily.com/news/computers_math/',
        'https://www.sciencedaily.com/news/space_time/',
    ]
    base_url = 'https://www.sciencedaily.com'

    def parse(self, response):
        headlines_segment = response.xpath("//div[@id='headlines']")
        news = headlines_segment.xpath("./ul/li/a")
        for link in news:
            yield response.follow(link, callback=self.parse_news)

        # TODO: another way could be iterate on news_by_dates, see if there are news for 'today' and just add them.
        # this is independent of 'Job' but for robustness we need to check links against database, add them until the
        # first duplicate link.
        news_by_dates = headlines_segment.xpath("./child::*")  # all tag/element children

    # noinspection PyMethodMayBeStatic
    def parse_news(self, response):
        loader: ItemLoader = ArticleLoader(item=Article(), response=response)
        loader.add_value('url', response.url)

        loader.add_xpath('title', "//h1[@id='headline']")
        loader.add_xpath('subtitle', "//h2[@id='subtitle']")  # optional

        loader.add_xpath('date', "//dd[@id='date_posted']")  #
        loader.add_xpath('source', "//dd[@id='source']")  #
        loader.add_xpath('summary', "//dd[@id='abstract']")

        loader.add_xpath('text', "//div[@id='text']/p")  # <p>s are joined in related 'Item Loader'

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        # see nesting loaders https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders
        source_segment_loader = loader.nested_xpath("//div[@id='story_source']/p[2]")
        source_segment_loader.add_xpath('source_url', "./a/strong/../@href")
        # optional
        source_segment_loader.add_xpath('source_article_url', "./a[contains(text(), 'Materials')]/@href")

        # print(l.load_item())
        yield loader.load_item()
