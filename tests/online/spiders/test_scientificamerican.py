import unittest

from scrapy import FormRequest

from tests.utils import real_response
from tests.unit.spiders.test_scientificamerican import TestScientificAmericanSpider

free_normal_article_url = "https://www.scientificamerican.com/article/shortcuts-in-covid-19-drug-research-could-do-long-term-harm-bioethicists-worry/"
free_featured_article_url = "https://www.scientificamerican.com/article/no-one-can-explain-why-planes-stay-in-the-air/"
paid_article_url = "https://www.scientificamerican.com/article/kilometers-of-dark-cable-form-the-newest-seismic-sensors/"


class TestScientificAmericanSpiderOnline(TestScientificAmericanSpider):
    def setUp(self) -> None:
        super(TestScientificAmericanSpiderOnline, self).setUp()

    def test_parse_online(self):
        response = real_response('https://www.scientificamerican.com/tech/')
        self.assertGreaterEqual(len(list(self.spider.parse(response))), 5)  # tech segment has 7 subtopics

    def test_parse_subtopic_online(self):
        # I really don't know why these lines get time-out and the other line doesn't
        # topic_page = real_response('https://www.scientificamerican.com/tech/')
        # subtopic_request = list(self.spider.parse(topic_page))[2]
        # response = real_response(subtopic_request)
        response = real_response(FormRequest("https://www.scientificamerican.com/computing/",
                                             formdata={'source': 'article'}))

        self.assertGreaterEqual(len(list(self.spider.parse_subtopic(response))), 10)

    # Paid articles are determined from SA based on your cookies. We don't consider them for online tests.
    def test_parse_news_normal_article(self):
        free_normal = real_response(free_normal_article_url)
        item = next(self.spider.parse_news(free_normal))
        self.assertEqual(len(item), 6)

    def test_parse_news_featured_article(self):
        free_featured = real_response(free_featured_article_url)
        item = next(self.spider.parse_news(free_featured))
        self.assertEqual(len(item), 6)


if __name__ == '__main__':
    unittest.main()
