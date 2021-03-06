from scrapy import Spider
from scrapy.loader import ItemLoader

from news_crawler.items import ArticleItem, LiveScienceArticleLoader


class LiveScienceSpider(Spider):
    name = 'livescience'
    allowed_domains = ['livescience.com']
    start_urls = [
        'https://www.livescience.com/technology',
        'https://www.livescience.com/health',
    ]
    custom_settings = {
        'SPIDERMON_VALIDATION_MODELS': ['news_crawler.validators.LiveScienceValidatorItem'],
    }

    def parse(self, response):
        latest_news = response.css("div#content section a.article-link")
        for link in latest_news:
            yield response.follow(link, callback=self.parse_news)

    # noinspection PyMethodMayBeStatic
    def parse_news(self, response):
        loader: ItemLoader = LiveScienceArticleLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        # see nesting loaders https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders
        article_loader = loader.nested_css("div#main article")

        article_loader.add_css('title', "header h1")
        article_loader.add_css('subtitle', "header p.strapline")

        article_loader.add_css('date', "header time::attr(datetime)")
        article_loader.add_css('author', "header span.by-author a > span")

        # TODO: source info
        # livescience are mostly originally published in livescience; those not, don't refer to exact source link.

        # <p>s are joined and filtered in related 'Item Loader'
        loader.add_css('content', "div#article-body > p")
        yield loader.load_item()
