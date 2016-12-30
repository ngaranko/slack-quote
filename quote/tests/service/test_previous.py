from django.test import TestCase
from django.utils import timezone

import quote.service

from quote.factories import QuoteFactory


class QuoteServicePreviousTestCase(TestCase):

    def test(self):
        """
        No records in database. Should return None
        """
        self.assertEqual(quote.service.previous(), None)

    def test_one_record(self):
        """
        One record in database, should return record
        """

        q = QuoteFactory()

        self.assertEqual(quote.service.previous(), q)

    def test_two_records(self):
        """
        Two records in database, should return first records two times, since the next
        function is not responsible for updating the last_hit field so sequence is unchanged
        """

        q = QuoteFactory()
        QuoteFactory()

        self.assertEqual(quote.service.previous(), q)
        self.assertEqual(quote.service.previous(), q)

    def test_two_records_sequence(self):
        """
        Two records in database, second records has a hit value, other does not. So it should return
        first record
        """

        q = QuoteFactory(last_hit=timezone.now())
        QuoteFactory()

        self.assertEqual(quote.service.previous(), q)
