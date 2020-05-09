import unittest
from datetime import datetime

from items import ScienceAlertLoader, ArticleItem
from spiders.sciencealert import ScienceAlertSpider
from tests.utils import fake_response, fake_response_by_body


# TODO: parameterize test for multiple article


class LiveScienceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = ScienceAlertSpider()

    def test_livescience_parse_news(self):
        response = fake_response('sciencealert-fake.html')
        item = next(self.spider.parse_news(response))
        self.assertEqual(item['title'],
                         "Could You Be an Asymptomatic COVID-19 Carrier? Here's What You Need to Know", )
        self.assertEqual(item['date'],  # 1 MAY 2020
                         datetime(2020, 5, 1, 0, 0, 0))
        self.assertEqual(item['author'],
                         'William Petri')

        content: str = item['content']
        #  TODO: check for tags existence. Parent Spider test case?
        # for word in ('<p', '<em', '<a', '<iframe', '<div', '<span' # tags should not be in content
        #              '')
        for word in ("William Petri, Professor of Medicine",  # no author info
                     "This article is republished",  # no source paragraph
                     "How common is it for people to contract and fight",  # no internal header/titles
                     ):
            self.assertNotIn(word, content)
        self.assertEqual(len(content.split('\n\n')), 25)
        self.assertEqual(content.split('\n\n')[0],
                         r"Blood tests that check for exposure to the coronavirus are starting to come online, "
                         r"and preliminary findings suggest that many people have been infected without knowing it.")

    # TODO: single parameterize test for both author_date formats
    def test_author_date_format1(self):
        response = fake_response_by_body("""
        <div class="author-name">
            <div class="author-name-text">
                <div class="author-name-name floatstyle">
                    <span>AMELIE BOTTOLLIER-DEPOIS, AFP </span>
                </div>
                <div class="author-name-date floatstyle">
                    <span>7 MAY 2020 </span>
                </div>
            </div>
        </div>""")
        loader = ScienceAlertLoader(item=ArticleItem(), response=response)
        spider = ScienceAlertSpider()
        item = spider.parse_author_date(loader).load_item()

        self.assertEqual(item['author'], 'Amelie Bottollier-Depois')
        self.assertEqual(item['date'], datetime(2020, 5, 7))

    def test_author_date_format2(self):
        response = fake_response_by_body("""
        <div class="author-name">
            <div class="author-name-text">
                <div class="author-name-name floatstyle">
                    <span>PETER ELLIS, MARK WASS &amp; MARTIN MICHAELIS, THE CONVERSATION </span>
                </div>
                <div class="author-name-date floatstyle">
                    <span>8 MAY 2020 </span>
                </div>
            </div>
        </div>
        """)
        loader = ScienceAlertLoader(item=ArticleItem(), response=response)
        spider = ScienceAlertSpider()
        item = spider.parse_author_date(loader).load_item()

        self.assertEqual(item['author'], 'Peter Ellis')
        self.assertEqual(item['date'], datetime(2020, 5, 8))


if __name__ == '__main__':
    unittest.main()
