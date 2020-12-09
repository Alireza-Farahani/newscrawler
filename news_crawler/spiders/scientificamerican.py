from scrapy import Spider, FormRequest
from scrapy.exceptions import DropItem
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

from news_crawler.items import ScientificAmericanLoader, ArticleItem


class ScientificAmericanSpider(Spider):
    name = 'scientificamerican'
    allowed_domains = ['scientificamerican.com']
    start_urls = [
        'https://www.scientificamerican.com/tech/',
        # 'https://www.scientificamerican.com/health/',
        # 'https://www.scientificamerican.com/the-sciences/',
    ]

    custom_settings = {
        'COOKIES_ENABLED': False,
        'SPIDERMON_VALIDATION_MODELS': ['news_crawler.validators.ScientificAmericanValidatorItem'],
    }

    def parse(self, response: TextResponse):
        sub_topics = response.css('#topic-list a::attr(href)').getall()
        for link in sub_topics:
            # ScientificAmerican lists all type including video and podcast. We do a filtering for articles only.
            yield FormRequest(link, formdata={'source': 'article'}, callback=self.parse_subtopic)

    def parse_subtopic(self, response: TextResponse):
        articles = response.css('div.panel div.section-latest h2 a')
        yield from response.follow_all(articles,
                                       callback=self.parse_news,
                                       meta={'dont_redirect': True, "handle_httpstatus_list": [301, 302, 303]})

    def parse_news(self, response: TextResponse):
        # featured article get in redirection loop by SA if cookies are disabled.
        # Example url: https://www.scientificamerican.com/article/no-one-can-explain-why-planes-stay-in-the-air/
        if response.status in [301, 302, 303]:
            self.logger.error(f'redirect code {response.status} for {response.url}!')
            yield self.handle_redirection(response)

        # TODO: maybe updating 'stats'
        if self.is_paid_article(response):
            return  # spider callback MOST return either a generator or a dict/item like object???

        loader: ItemLoader = ScientificAmericanLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        # featured articles have different layout e.g.
        if self.is_featured_article(response):
            yield self.load_featured_article(loader)
        else:
            yield self.load_normal_article(loader)

    def handle_redirection(self, response: TextResponse):
        # manually set cookies for next request
        # https://stackoverflow.com/questions/36443246/how-to-get-cookie-from-scrapy-response-and-set-the-cookie-to-the-next-request
        # TODO: send/log error
        raise DropItem("redirection not handled for Scientific America yet.")

    # noinspection PyMethodMayBeStatic
    def is_paid_article(self, response: TextResponse):
        return response.css(".paywall")

    # noinspection PyMethodMayBeStatic
    def is_featured_article(self, response: TextResponse):
        return response.css('.feature-article-wrapper')

    # noinspection PyMethodMayBeStatic
    def load_normal_article(self, loader: ItemLoader) -> ArticleItem:
        article_header_loader: ItemLoader = loader.nested_css('#sa_body article header')
        article_header_loader.add_css('title', '.t_article-title')
        article_header_loader.add_css('subtitle', '.t_article-subtitle')
        article_header_loader.add_css('author', 'span[itemprop="author"] a')
        article_header_loader.add_css('date', '*[itemprop="datePublished"]')
        article_body_loader: ItemLoader = loader.nested_css('#sa_body article section')
        article_body_loader.add_css('content', 'div.mura-region-local > p')
        return loader.load_item()

    # noinspection PyMethodMayBeStatic
    def load_featured_article(self, loader: ItemLoader) -> ArticleItem:
        article_header_loader: ItemLoader = loader.nested_css('.feature-article--header')
        article_header_loader.add_css('title', '*[itemprop="headline"]')
        article_header_loader.add_css('subtitle', '.t_article-subtitle')
        loader.add_css('author', '.author-bio .tx_article-rightslink > strong > a')
        article_header_loader.add_css('date', '*[itemprop="datePublished"]')

        loader.add_css('content', 'div.mura-region-local > p')
        return loader.load_item()
