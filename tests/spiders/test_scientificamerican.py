import unittest
from datetime import date

from items import ScientificAmericanLoader, ArticleItem
from spiders.scientificamerican import ScientificAmericanSpider
from tests.utils import fake_response


class TestScienceNewsSpider(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = ScientificAmericanSpider()
        # https://www.scientificamerican.com/article/heat-and-humidity-are-already-reaching-the-limits-of-human-tolerance
        self.free_normal_article = fake_response('scientificamerican-example.html')
        # https://www.scientificamerican.com/article/no-one-can-explain-why-planes-stay-in-the-air/
        self.free_featured_article = fake_response('scientificamerican-example-featured.html')
        # https://www.scientificamerican.com/article/kilometers-of-dark-cable-form-the-newest-seismic-sensors/
        self.paid_article = fake_response('scientificamerican-example-paid.html')

    def test_is_paid_article(self):
        self.assertFalse(self.spider.is_paid_article(self.free_normal_article))
        self.assertFalse(self.spider.is_paid_article(self.free_featured_article))
        self.assertTrue(self.spider.is_paid_article(self.paid_article))

    def test_is_featured_article(self):
        self.assertFalse(self.spider.is_featured_article(self.free_normal_article))
        self.assertFalse(self.spider.is_featured_article(self.paid_article))
        self.assertTrue(self.spider.is_featured_article(self.free_featured_article))

    def test_parse_normal_article(self):
        loader = ScientificAmericanLoader(item=ArticleItem(), response=self.free_normal_article)
        item = self.spider.load_normal_article(loader)

        self.assertEqual(item['title'],
                         "Shortcuts in COVID-19 Drug Research Could Do Long-Term Harm, Bioethicists Worry")
        self.assertEqual(item['subtitle'],
                         "Compassionate use of experimental medicine needs to coexist with scientific rigor to help "
                         "patients, researchers write in the journal Science")
        self.assertEqual(item['author'], "Anna Kuchment")
        self.assertEqual(item['date'], date(2020, 4, 24))

        content: str = item['content']
        for word in ("Read more about",  # no extra info
                     ):
            self.assertNotIn(word, content)

        content_pars = content.split('\n\n')
        self.assertEqual(len(content_pars), 19)
        self.assertTrue(content_pars[0].startswith("Does a widespread medical emergency justify speedier,"))
        self.assertNotIn('', content_pars)  # no empty paragraph

    def test_parse_featured_article(self):
        loader = ScientificAmericanLoader(item=ArticleItem(), response=self.free_featured_article)
        item = self.spider.load_featured_article(loader)

        self.assertEqual(item['title'],
                         "No One Can Explain Why Planes Stay in the Air")
        self.assertEqual(item['subtitle'],
                         "Do recent explanations solve the mysteries of aerodynamic lift?")
        self.assertEqual(item['author'], "Ed Regis")
        self.assertEqual(item['date'], date(2020, 2, 1))

        content: str = item['content']
        for word in ("Read more about",  # no extra info
                     ):
            self.assertNotIn(word, content)

        content_pars = content.split('\n\n')
        self.assertEqual(len(content_pars), 38)
        self.assertTrue(content_pars[0].startswith("In December 2003, to commemorate the 100th anniversary of the"))
        self.assertNotIn('', content_pars)  # no empty paragraph

    def test_parse_news(self):
        # logic already tested in above test methods
        item = next(self.spider.parse_news(self.free_normal_article))
        self.assertEqual(len(item), 6)

        item = next(self.spider.parse_news(self.free_featured_article))
        self.assertEqual(len(item), 6)

        item = next(self.spider.parse_news(self.paid_article))
        self.assertIsNone(item, ArticleItem)
