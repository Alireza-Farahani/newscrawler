import unittest
from datetime import datetime, timezone

from spiders.livescience import LiveScienceSpider
from tests.utils import fake_response


# TODO: parameterize test for multiple article
class LiveScienceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = LiveScienceSpider()

    def test_livescience_parse_news(self):
        response = fake_response('livescience-fake.html')
        item = next(self.spider.parse_news(response))
        self.assertEqual(item['title'],
                         "5G is not linked to the coronavirus pandemic in any way. Here's the science.", )
        self.assertEqual(item['subtitle'],
                         "Peddling such misinformation is not only wrong, it's destructive.", )
        self.assertEqual(item['date'],  # 2020-04-09T18:26:28Z
                         datetime(2020, 4, 9, 18, 26, 28, tzinfo=timezone.utc))
        self.assertEqual(item['author'],
                         'Stanley Shanapinda')

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
