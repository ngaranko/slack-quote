from django.test import TestCase

import quote.service as quote_service

from quote.factories import QuoteFactory


class QuoteServiceHitTestCase(TestCase):

    def setUp(self):

        self.quote = QuoteFactory()
        self.assertEqual(self.quote.hit_count, 0)
        self.assertIsNone(self.quote.last_hit)
        self.assertEqual(self.quote.author.hit_count, 0)
        self.assertIsNone(self.quote.author.last_hit)

    def test(self):

        quote_service.hit(quote=self.quote)

        self.quote.refresh_from_db()
        self.quote.author.refresh_from_db()

        self.assertEqual(self.quote.hit_count, 1)
        self.assertIsNotNone(self.quote.last_hit)
        self.assertEqual(self.quote.author.hit_count, 1)
        self.assertIsNotNone(self.quote.author.last_hit)

    def test_hit_twice(self):

        quote_service.hit(quote=self.quote)
        quote_service.hit(quote=self.quote)

        self.quote.refresh_from_db()
        self.quote.author.refresh_from_db()

        self.assertEqual(self.quote.hit_count, 2)
        self.assertEqual(self.quote.author.hit_count, 2)
