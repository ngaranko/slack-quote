from django.test import Client
from django.test import TestCase

from quote.factories import QuoteFactory


class TestAPIView(TestCase):

    def setUp(self):

        self.quote = QuoteFactory()
        self.client = Client()
        self.payload = {
            'token': 'FKPUJkhcrVgK4jhppawRoEDR',
            'team_id': 'T0001',
            'team_domain': 'example',
            'channel_id': 'C2147483705',
            'channel_name': 'test',
            'user_id': 'U2147483697',
            'user_name': 'friend',
            'command': '/quote',
            'text': '94070',
            'response_url': 'https://hooks.slack.com/commands/1234/5678'
        }

    def test(self):

        response = self.client.post('/api/', self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'response_type': 'in_channel', 'text': '', 'attachments': []})

    def test_text(self):

        self.quote.text = 'test'
        self.quote.save()

        response = self.client.post('/api/', self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['text'], self.quote.text)

    def test_context(self):

        self.quote.context = 'test'
        self.quote.save()

        response = self.client.post('/api/', self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['attachments'][0]['text'], self.quote.context)
