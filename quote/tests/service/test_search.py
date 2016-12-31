from django.test import TestCase

import quote.service as quote_service

from quote.factories import QuoteFactory


class QuoteServicePreviousTestCase(TestCase):

    def setUp(self):

        self.first_quote = QuoteFactory(
            text='Wrong quote',
            context='Wrong quote',
            text_english='Wrong quote',
            context_english='Wrong quote'
        )

        self.good_quote = QuoteFactory(
            text='text_native',
            context='context_native',
            text_english='text_english',
            context_english='context_english'
        )

    def test(self):

        quote = quote_service.search('something_not_existing')

        self.assertEqual(quote, None)

    def test_parameter_only(self):

        quote = quote_service.search('--some-parameter')

        self.assertEqual(quote, None)

    def test_text(self):

        quote = quote_service.search('text_native')

        self.assertEqual(quote, self.good_quote)

    def test_context(self):
        quote = quote_service.search('context_native')

        self.assertEqual(quote, self.good_quote)

    def test_text_english(self):
        quote = quote_service.search('text_english')

        self.assertEqual(quote, self.good_quote)

    def test_context_english(self):
        quote = quote_service.search('context_english')

        self.assertEqual(quote, self.good_quote)
