from django.test import TestCase
from django.utils import timezone

import quote.service

from quote.factories import QuoteFactory


class QuoteServiceNextTestCase(TestCase):

    def test(self):
        """
        No records in database. Should return None
        """
        self.assertEqual(quote.service.next(), None)

    def test_one_record(self):
        """
        One record in database, should return record
        """

        q = QuoteFactory()

        self.assertEqual(quote.service.next(), q)

    def test_two_records(self):
        """
        Two records in database, should return first records two times, since the next
        function is not responsible for updating the last_hit field so sequence is unchanged
        """

        q = QuoteFactory()
        QuoteFactory()

        self.assertEqual(quote.service.next(), q)
        self.assertEqual(quote.service.next(), q)

    def test_two_records_sequence(self):
        """
        Two records in database, first records has a hit value, other does not. So it should return
        second record
        """

        QuoteFactory(last_hit=timezone.now())
        q = QuoteFactory()

        self.assertEqual(quote.service.next(), q)
