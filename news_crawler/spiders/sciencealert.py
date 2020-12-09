from scrapy import Spider
from scrapy.http import Response, TextResponse
from scrapy.loader import ItemLoader

from news_crawler.items import ArticleItem, ScienceAlertLoader


class ScienceAlertSpider(Spider):
    name = 'sciencealert'
    allowed_domains = ['sciencealert.com']
    start_urls = [
        'https://www.sciencealert.com/health',
        'https://www.sciencealert.com/tech',
        # 'https://www.sciencealert.com/physics',
    ]
    custom_settings = {
        'SPIDERMON_VALIDATION_MODELS': ['news_crawler.validators.ScienceAlertValidatorItem'],
    }

    def parse(self, response: Response):
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

        self.parse_author_date(article_loader)

        body_loader = article_loader.nested_css("div.article-fulltext")
        body_loader.add_css('content', "p")  # <p>s are joined in related 'Item Loader'

        # TODO: source and source_article e.g.
        # https://www.sciencealert.com/scientists-have-built-robots-entirely-out-of-living-frog-cells

        yield loader.load_item()

    @staticmethod
    def parse_author_date(loader: ScienceAlertLoader) -> None:
        # some articles have date in div.author-name-name! e.g.
        # https://www.sciencealert.com/us-life-expectancy-just-increased-for-the-first-time-in-4-years
        # So in these cases we pick second 'author-name-name'
        if len(loader.get_css("div.author-name-date span")) == 1:
            author_css = "div.author-name-name span"
            date_css = "div.author-name-date span"
        else:
            author_css = "div.author-name-name:first-child span"
            date_css = "div.author-name-name:last-child span"
        loader.add_css('date', date_css)
        loader.add_css('author', author_css)  # cases of 'author, corporation' handled in related item loader
