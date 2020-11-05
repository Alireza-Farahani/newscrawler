import unittest
from datetime import datetime
from datetime import timezone

from scrapy.http import Response

from spiders.livescience import LiveScienceSpider
from tests.utils import fake_response


# TODO: parameterize test for multiple article
class TestLiveScienceSpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = LiveScienceSpider()

    def test_parse_news(self):
        # response fetched from https://www.livescience.com/5g-coronavirus-conspiracy-theory-debunked.html
        response = fake_response('livescience-example.html')
        self._test_parse_news(response)

    def _test_parse_news(self, response: Response):
        item = next(self.spider.parse_news(response))
        self.assertEqual(item['title'],
                         "5G is not linked to the coronavirus pandemic in any way. Here's the science.", )
        self.assertEqual(item['subtitle'],
                         "Peddling such misinformation is not only wrong, it's destructive.", )
        self.assertEqual(item['date'], datetime(2020, 4, 9))  # 2020-04-09T18:26:28Z
        self.assertEqual(item['author'], 'Stanley Shanapinda')

        content: str = item['content']
        for word in ('conspiracy', '(and viewed more than 668,000 times)'):
            self.assertIn(word, content)
        #  TODO: check for tags existence. Parent Spider test case?
        # for word in ('<p', '<em', '<a', '<iframe', '<div', '<span' # tags should not be in content
        #              '')
        for word in ("OFFER: Save",  # no promotional content
                     "This article was originally",  # no source paragraph
                     "Read more:",  # no link to other articles
                     "Celebrities - stick to what you know",  # no internal header/titles
                     ):
            self.assertNotIn(word, content)
        self.assertEqual(len(content.split('\n\n')), 25)


if __name__ == '__main__':
    unittest.main()
