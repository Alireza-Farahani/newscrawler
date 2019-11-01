import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset-spider"
    start_urls = ['http://brickset.com/sets/year-2019']

    def parse(self, response):
        set_selector = '.set'
        for brickset in response.css(set_selector):
            name_selector = 'h1 ::text'
            pieces_selector = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            minifigs_selector = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            image_selector = 'img ::attr(src)'
            yield {
                'name': brickset.css(name_selector).extract_first(),
                'pieces': brickset.xpath(pieces_selector).extract_first(),
                'minifigs': brickset.xpath(minifigs_selector).extract_first(),
                'image': brickset.css(image_selector).extract_first(),
            }

        # next_page_selector = '.next a ::attr(href)'
        # next_page = response.css(next_page_selector).extract_first()
        # if next_page:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback=self.parse
        #     )
