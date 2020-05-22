from itertools import chain

from scrapy import Spider
from scrapy.http import TextResponse

from sarbazi_crawler.items import ScienceNewsLoader, ArticleItem


class ScienceNewsSpider(Spider):
    name = 'sciencenews'
    allowed_domains = ['sciencenews.org']
    start_urls = [
        'https://www.sciencenews.org/topic/tech',
    ]

    def parse(self, response: TextResponse):
        latest_articles = response.css('main#content article[class*="expanded-feature"] *[class*="title"] a')
        more_stories = response.css('ol[class*="list"] *[class*="title"] a')
        yield from response.follow_all(chain(latest_articles, more_stories), callback=self.parse_news)

    # noinspection PyMethodMayBeStatic
    def parse_news(self, response: TextResponse):
        loader = ScienceNewsLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        header_loader = loader.nested_css('main#content article header')
        header_loader.add_css('title', 'h1')
        header_loader.add_css('subtitle', 'h2')
        self.parse_author_date(loader)
        loader.add_css('content', 'main#content .content .rich-text > p')

        yield loader.load_item()

    # noinspection PyMethodMayBeStatic
    def parse_author_date(self, loader: ScienceNewsLoader):
        # column article have different layout.
        # e.g. https://www.sciencenews.org/article/will-to-survive-might-take-artificial-intelligence-next-level
        if len(loader.get_css('main#content article header.is-column')) > 0:
            author_date_container = 'main#content article header *[class*="column-meta"] '
            author_css = author_date_container + '*[class*="heading"] a'
            date_css = author_date_container + '*[class*="timestamp"] time::attr(datetime)'
        else:
            author_css = '*[class*="authors"] .author a'
            date_css = 'time.date::attr(datetime)'
        loader.add_css('date', date_css)
        loader.add_css('author', author_css)
