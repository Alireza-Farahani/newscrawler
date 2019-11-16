from scrapy import Spider


class ScienceDailyArticleSpider(Spider):
    name = 'science_daily_article'
    allowed_domains = ['sciencedaily.com']
    start_urls = ['https://www.sciencedaily.com/releases/2019/10/191031100516.htm',
                  'https://www.sciencedaily.com/releases/2019/11/191114124048.htm']

    def parse(self, response):
        title: str = response.xpath("//h1[@id='headline']/text()").get()
        subtitle: str = response.xpath("//h2[@id='subtitle']/text()").get()

        date: str = response.xpath("//dd[@id='date_posted']/text()").get()  # ::before dare. check konesh
        source: str = response.xpath("//dd[@id='source']/text()").get()  # in ham ::before dare. check konesh
        summary: str = response.xpath("//dd[@id='abstract']/text()").get()  # in ham ::before dare. check konesh

        text = response.xpath("//div[@id='text']/text()").get()  # concat <p>s todo:type hint. item pipeline

        # it's possible that source article link not exists.
        # second child <p> of <div id=story_source> can have links to story direct link and source provider link
        # e.g. tabnak.ir/n/123 and tabnak.ir
        # todo: ensure direct link is selected
        source_link = response.xpath("//div[@id='story_source']//a/strong/text()")
