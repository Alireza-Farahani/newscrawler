import unittest
from datetime import date
from typing import List

from scrapy.http import TextResponse

from items import ScienceNewsLoader, ArticleItem
from spiders.sciencenews import ScienceNewsSpider
from tests.utils import fake_response, real_response


class TestScienceNewsSpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = ScienceNewsSpider()

    def test_parse_news_offline(self):
        # response fetched from
        # https://www.sciencenews.org/article/coronavirus-covid-19-proteins-super-computer-fight-pandemic
        response = fake_response('sciencenews-example.html')
        self._test_parse_news(response)

    def test_parse_news_online(self):
        response = real_response("https://www.sciencenews.org/article/coronavirus-covid-19-proteins-super-computer-fight-pandemic")
        self._test_parse_news(response)

    def _test_parse_news(self, response: TextResponse):
        item = next(self.spider.parse_news(response))

        self.assertEqual(item['title'],
                         "You can help fight the coronavirus. All you need is a computer")
        self.assertEqual(item['subtitle'],
                         "Donating computing time can help create a virtual supercomputer that can search for a cure")
        self.assertEqual(item['author'], "Maria Temming")
        self.assertEqual(item['date'], date(2020, 3, 25))

        content_pars: List[str] = item['content'].split('\n\n')
        self.assertEqual(len(content_pars), 14)
        self.assertEqual(content_pars[0], "Staying home isn’t the only way to help fight the coronavirus pandemic.")
        self.assertNotIn('\n', content_pars[1])  # ensure no unnecessary new line

    def test_author_date_featured_article_offline(self):
        # response fetched from https://www.sciencenews.org/article/susan-milius-your-guide-peculiarities-nature
        response = fake_response('sciencenews-example-featured.html')
        self._test_author_date_featured_article(response)

    def test_author_date_featured_article_online(self):
        response = real_response("https://www.sciencenews.org/article/susan-milius-your-guide-peculiarities-nature")
        self._test_author_date_featured_article(response)

    # TODO: single parameterize test for both author_date formats
    def _test_author_date_featured_article(self, response: TextResponse):
        loader = ScienceNewsLoader(item=ArticleItem(), response=response)
        self.spider.parse_author_date(loader)
        item = loader.load_item()

        self.assertEqual(item['author'], 'Nancy Shute')
        self.assertEqual(item['date'], date(2020, 4, 19))

    # -----------------------------------------------------------------------------------------
    def test_parse_online(self):
        response = real_response('https://www.sciencenews.org/topic/tech')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 10)


if __name__ == '__main__':
    unittest.main()
