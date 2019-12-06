from scrapy import Spider

from sarbazi_crawler.items import Article


class ScienceDailyArticleSpider(Spider):
    name = 'science_daily_article'
    allowed_domains = ['sciencedaily.com']
    start_urls = ['https://www.sciencedaily.com/releases/2019/10/191031100516.htm',
                  'https://www.sciencedaily.com/releases/2019/11/191114124048.htm']

    def parse(self, response):
        title: str = response.xpath("//h1[@id='headline']/text()").get()
        subtitle: str = response.xpath("//h2[@id='subtitle']/text()").get()  # optional

        date: str = response.xpath("//dd[@id='date_posted']/text()").get()  # ::before dare. check konesh
        source: str = response.xpath("//dd[@id='source']/text()").get()  # in ham ::before dare. check konesh
        summary: str = response.xpath("//dd[@id='abstract']/text()").get()  # in ham ::before dare. check konesh

        text = response.xpath("//div[@id='text']")  # concat <p>s todo:type hint. item pipeline

        # see nesting selectors https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
        source_segment = response.xpath("//div[@id='story_source']/p[2]")
        source_url = source_segment.xpath("./a/strong/../@href").get()
        source_article_url = source_segment.xpath("./a[contains(text(), 'Materials')]/@href").get()

        article = Article(url=response.url, title=title, subtitle=subtitle, date=date, source=source, summary=summary,
                          text=text, source_url=source_url, source_article_url=source_article_url)
        print(article)
