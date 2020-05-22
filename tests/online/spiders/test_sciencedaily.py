import unittest

from tests.utils import real_response
from unit.spiders.test_sciencedaily import TestScienceDailySpider


class TestScienceDailySpiderOnline(TestScienceDailySpider):
    def setUp(self) -> None:
        super(TestScienceDailySpiderOnline, self).setUp()

    def test_parse_online(self):
        response = real_response('https://www.sciencedaily.com/news/computers_math/')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 34)  # ensuring all 3 segments are selected

    def test_parse_news(self):
        response = real_response("https://www.sciencedaily.com/releases/2020/05/200507194907.htm")
        self._test_parse_news(response)


if __name__ == '__main__':
    unittest.main()
