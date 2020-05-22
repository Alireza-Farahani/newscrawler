import unittest

from tests.utils import real_response
from unit.spiders.test_sciencenews import TestScienceNewsSpider


class TestScienceNewsSpiderOnline(TestScienceNewsSpider):
    def setUp(self) -> None:
        super(TestScienceNewsSpiderOnline, self).setUp()

    def test_parse_online(self):
        response = real_response('https://www.sciencenews.org/topic/tech')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 10)

    def test_parse_news(self):
        response = real_response(
            "https://www.sciencenews.org/article/coronavirus-covid-19-proteins-super-computer-fight-pandemic")
        self._test_parse_news(response)

    def test_author_date_featured_article(self):
        response = real_response("https://www.sciencenews.org/article/susan-milius-your-guide-peculiarities-nature")
        self._test_author_date_featured_article(response)


if __name__ == '__main__':
    unittest.main()
