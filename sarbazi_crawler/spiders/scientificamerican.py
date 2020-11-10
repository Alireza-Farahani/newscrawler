from scrapy import Spider, FormRequest
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import ScientificAmericanLoader, ArticleItem


# SA = scientific american
class ScientificAmericanSpider(Spider):
    name = 'scientificamerican'
    allowed_domains = ['scientificamerican.com']
    start_urls = [
        'https://www.scientificamerican.com/tech/',
        # 'https://www.scientificamerican.com/health/'
        # 'https://www.scientificamerican.com/computing/',
    ]

    def parse(self, response: TextResponse):
        sub_topics = response.css('#topic-list a::attr(href)').getall()
        for link in sub_topics:
            # SA lists all type including video and podcast. We do a filtering like what website does for articles only.
            yield FormRequest(link, formdata={'source': 'article'}, callback=self.parse_subtopic)

    def parse_subtopic(self, response: TextResponse):
        articles = response.css('div.panel div.section-latest h2 a')
        yield from response.follow_all(articles, callback=self.parse_news, )

    def parse_news(self, response: TextResponse):
        # TODO: maybe updating 'stats'
        if self.is_paid_article(response):
            yield  # spider callback MOST return either a generator or a dict/item like object
        else:
            loader: ItemLoader = ScientificAmericanLoader(item=ArticleItem(), response=response)
            loader.add_value('url', response.url)

            if not self.is_featured_article(response):
                yield self.load_normal_article(loader)
            else:  # some featured articles have different layout e.g.
                # TODO recursive redirection when using scrapy
                # https://www.scientificamerican.com/article/no-one-can-explain-why-planes-stay-in-the-air/
                # print("---**------------ThErE!-----------**-")
                yield self.load_featured_article(loader)

    # noinspection PyMethodMayBeStatic
    def is_paid_article(self, response: TextResponse):
        return response.css("aside.paywall")

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
