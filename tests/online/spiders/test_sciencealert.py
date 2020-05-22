import unittest

from tests.utils import real_response
from unit.spiders.test_sciencealert import TestScienceAlertSpider


class TestScienceAlertSpiderOnline(TestScienceAlertSpider):
    def setUp(self) -> None:
        super(TestScienceAlertSpiderOnline, self).setUp()

    def test_parse(self):
        response = real_response('https://www.sciencealert.com')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 10)

    def test_parse_news(self):
        response = real_response(
            "https://www.sciencealert.com/a-physician-answers-5-questions-about-asymptomatic-covid-19")
        self._test_parse_news(response)


if __name__ == '__main__':
    unittest.main()
