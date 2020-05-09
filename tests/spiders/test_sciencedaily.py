import unittest
from datetime import date

from spiders.sciencedaily import ScienceDailySpider
from tests.utils import fake_response


class TestScienceDailySpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = ScienceDailySpider()

    def test_parse_news(self):
        # response fetched from https://www.sciencedaily.com/releases/2020/05/200507194907.htm
        response = fake_response('sciencedaily-example.html')
        item = next(self.spider.parse_news(response))

        self.assertEqual(item['title'],
                         "Blood thinners may improve survival among hospitalized COVID-19 patients")
        self.assertEqual(item['subtitle'],
                         "Research could change standard of care protocols to prevent clotting associated with "
                         "coronavirus")

        self.assertEqual(item['date'], date(2020, 5, 7))
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
