from scrapy import Spider
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import Article, ArticleLoader


class ScienceDailyArticleSpider(Spider):
    name = 'science_daily_article'
    allowed_domains = ['sciencedaily.com']
    start_urls = ['https://www.sciencedaily.com/releases/2019/10/191031100516.htm',
                  'https://www.sciencedaily.com/releases/2019/11/191114124048.htm']

    def parse(self, response):
        l: ItemLoader = ArticleLoader(item=Article(), response=response)
        l.add_value('url', response.url)

        l.add_xpath('title', "//h1[@id='headline']")
        l.add_xpath('subtitle', "//h2[@id='subtitle']")  # optional

        l.add_xpath('date', "//dd[@id='date_posted']")  #
        l.add_xpath('source', "//dd[@id='source']")  #
        l.add_xpath('summary', "//dd[@id='abstract']")

        l.add_xpath('text', "//div[@id='text']/p")  # <p>s are joined in related 'Item Loader'

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        # see nesting loaders https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders
        source_segment_loader = l.nested_xpath("//div[@id='story_source']/p[2]")
        source_segment_loader.add_xpath('source_url', "./a/strong/../@href")
        # optional
        source_segment_loader.add_xpath('source_article_url', "./a[contains(text(), 'Materials')]/@href")

        # print(l.load_item())
        yield l.load_item()
