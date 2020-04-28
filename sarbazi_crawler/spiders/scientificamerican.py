from scrapy import Spider, FormRequest
from scrapy.http import TextResponse
# SA = scientific american
from scrapy.loader import ItemLoader

from sarbazi_crawler.items import ScientificAmericanLoader, ArticleItem


class ScientificAmerican(Spider):
    name = 'scientificamerican'
    allowed_domains = ['scientificamerican.com']
    start_urls = [
        'https://www.scientificamerican.com/tech/',
        # 'https://www.scientificamerican.com/health/'
        # 'https://www.scientificamerican.com/computing/',
    ]

    def parse(self, response: TextResponse):
        sub_topics = response.xpath('//*[@id="topic-list"]//a/@href').getall()
        for link in sub_topics:
            # SA lists all type including video and podcast. We do a filtering like what website does for articles only.
            yield FormRequest(link, formdata={'source': 'article'}, callback=self.parse_subtopic)

    def parse_subtopic(self, response: TextResponse):
        articles = response.css('div.panel div.section-latest h2 a')
        yield from response.follow_all(articles, callback=self.parse_news, )  # meta={'dont_redirect': True}

    def parse_news(self, response: TextResponse):
        loader: ItemLoader = ScientificAmericanLoader(item=ArticleItem(), response=response)
        loader.add_value('url', response.url)

        if len(response.css('.feature-article-wrapper')) == 0:
            yield self.parse_normal_article(loader)
        else:  # some featured articles have different layout e.g.
            pass  # TODO recursive redirection when using scrapy
            # https://www.scientificamerican.com/article/no-one-can-explain-why-planes-stay-in-the-air/
            # print("---**------------ThErE!-----------**-")
            # yield self.parse_feature_article(loader)

    def parse_normal_article(self, loader):
        article_header_loader: ItemLoader = loader.nested_xpath('//*[@id="sa_body"]//article//header')
        article_header_loader.add_css('title', '.t_article-title')
        article_header_loader.add_css('subtitle', '.t_article-subtitle')
        article_header_loader.add_xpath('author', '//span[@itemprop="author"]//a')
        article_header_loader.add_xpath('date', '//*[@itemprop="datePublished"]')
        article_body_loader: ItemLoader = loader.nested_xpath('//*[@id="sa_body"]//article//section')
        article_body_loader.add_css('content', 'div.mura-region-local > p')
        return loader.load_item()

    def parse_feature_article(self, loader):
        article_header_loader: ItemLoader = loader.nested_css('.feature-article--header')
        article_header_loader.add_xpath('title', '//*[@itemprop="headline"]')
        article_header_loader.add_css('subtitle', '.t_article-subtitle')
        loader.add_css('author', '.author-bio .tx_article-rightslink > strong > a')
        article_header_loader.add_xpath('date', '//*[@itemprop="datePublished"]')

        return loader.add_css('content', 'div.mura-region-local > p')
