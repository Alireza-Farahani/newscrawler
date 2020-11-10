import unittest

from tests.utils import real_response
from tests.unit.spiders.test_livescience import TestLiveScienceSpider


class TestLiveScienceSpiderOnline(TestLiveScienceSpider):
    def setUp(self) -> None:
        super(TestLiveScienceSpiderOnline, self).setUp()

    def test_parse(self):
        response = real_response('https://www.livescience.com')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 10)

    def test_parse_news(self):
        response = real_response("https://www.livescience.com/5g-coronavirus-conspiracy-theory-debunked.html")
        self._test_parse_news(response)


if __name__ == '__main__':
    unittest.main()
