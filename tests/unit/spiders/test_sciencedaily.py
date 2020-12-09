import unittest
from datetime import datetime

from scrapy.http import TextResponse

from news_crawler.spiders.sciencedaily import ScienceDailySpider
from tests.utils import fake_response


class TestScienceDailySpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = ScienceDailySpider()

    def test_parse_news(self):
        # response fetched from https://www.sciencedaily.com/releases/2020/05/200507194907.htm
        response = fake_response('sciencedaily-example.html')
        self._test_parse_news(response)

    def _test_parse_news(self, response: TextResponse):
        item = next(self.spider.parse_news(response))

        self.assertEqual(item['title'],
                         "Blood thinners may improve survival among hospitalized COVID-19 patients")
        self.assertEqual(item['subtitle'],
                         "Treating hospitalized COVID-19 patients with anticoagulants -- blood thinners that slow "
                         "down clotting -- may improve their chances of survival, researchers report. The study could "
                         "provide new insight on how to treat and manage coronavirus patients once they are admitted "
                         "to the hospital.")

        self.assertEqual(item['date'], datetime(2020, 5, 7))
        self.assertEqual(item['source'], "The Mount Sinai Hospital / Mount Sinai School of Medicine")
        self.assertEqual(item['source_article_url'],
                         "https://www.mountsinai.org/about/newsroom/2020/blood-thinners-may-improve-survival-among"
                         "-hospitalized-covid19-patients-pr")

        content: str = item['content']
        for word in ("William Petri, Professor of Medicine",  # no author info
                     "This article is republished",  # no source paragraph
                     "How common is it for people to contract and fight",  # no internal header/titles
                     ):
            self.assertNotIn(word, content)
        self.assertEqual(len(content.split('\n\n')), 10)
        self.assertTrue(content.split('\n\n')[0].startswith('The study found that hospitalized COVID-19 patients'))


if __name__ == '__main__':
    unittest.main()
