from django.test import Client
from django.test import TestCase

from quote.factories import QuoteFactory, AuthorFactory
from tile.factories import TileFactory, TemplateFactory


class TestAPIView(TestCase):

    def setUp(self):

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
        """
        No quote available
        """

        response = self.client.post('/api/', self.payload).json()

        self.assertDictEqual(response, {
            'response_type': 'in_channel',
            'text': 'No quote in database - System message',
            'attachments': []
        })

    def test_english_parameter(self):

        self.payload.update(text='--english')

        response = self.client.post('/api/', self.payload)

        self.assertEqual(response.status_code, 200)

    def test_payload_invalid(self):
        """
        If payload is invalid, empty 400 response should be send
        """

        # Make payload invalid by removing important key
        del self.payload['team_domain']

        response = self.client.post('/api/', self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {})

    def test_hit_count(self):
        quote = QuoteFactory()

        self.client.post('/api/', self.payload)

        quote.refresh_from_db()

        self.assertEqual(quote.hit_count, 1)

    def test_last_hit(self):
        quote = QuoteFactory()

        self.client.post('/api/', self.payload)

        quote.refresh_from_db()

        self.assertIsNotNone(quote.last_hit)

    def test_hit_count_author(self):
        quote = QuoteFactory()

        self.client.post('/api/', self.payload)

        quote.author.refresh_from_db()

        self.assertEqual(quote.author.hit_count, 1)

    def test_last_hit_author(self):
        quote = QuoteFactory()

        self.client.post('/api/', self.payload)

        quote.author.refresh_from_db()

        self.assertIsNotNone(quote.author.last_hit)

    def test_text(self):

        quote = QuoteFactory(text='test')

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['text'], '{} - {}'.format(quote.text, quote.author.name))

    def test_text_english(self):

        quote = QuoteFactory(text='test', text_english='text-english')

        self.payload['text'] += ' --english'

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['text'], '{} - {}'.format(quote.text_english, quote.author.name))

    def test_context(self):

        quote = QuoteFactory(context='test')

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['text'], quote.context)

    def test_context_english(self):

        quote = QuoteFactory(context='test', context_english='context-english')

        self.payload['text'] += ' --english'

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['text'], quote.context_english)

    def test_image(self):

        quote = QuoteFactory(image='test.jpg')

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['image_url'], 'http://testserver/{}'.format(quote.image))
        self.assertEqual(response['attachments'][0]['thumb_url'], 'http://testserver/{}'.format(quote.image))

        # If quote has no context a space is sent as text. Slack will not show image otherwise
        self.assertEqual(response['attachments'][0]['text'], ' ')

    def test_image_with_context(self):

        quote = QuoteFactory(image='test.jpg', context='test')

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['image_url'], 'http://testserver/{}'.format(quote.image))
        self.assertEqual(response['attachments'][0]['thumb_url'], 'http://testserver/{}'.format(quote.image))

        # If quote has no context a space is sent as text. Slack will not show image otherwise
        self.assertEqual(response['attachments'][0]['text'], quote.context)

    def test_tile(self):

        tile = TileFactory(
            quote_id=QuoteFactory().pk,
            template_id=TemplateFactory().pk,
            image='test.jpg'
        )

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['image_url'], 'http://testserver/{}'.format(tile.image))
        self.assertEqual(response['attachments'][0]['thumb_url'], 'http://testserver/{}'.format(tile.image))

        # Is always a space
        self.assertEqual(response['attachments'][0]['text'], ' ')

    def test_tile_english_false(self):

        tile = TileFactory(
            quote_id=QuoteFactory().pk,
            template_id=TemplateFactory().pk,
            image='test.jpg',
            english=False
        )

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['image_url'], 'http://testserver/{}'.format(tile.image))
        self.assertEqual(response['attachments'][0]['thumb_url'], 'http://testserver/{}'.format(tile.image))

        # Is always a space
        self.assertEqual(response['attachments'][0]['text'], ' ')

    def test_tile_english_true(self):

        tile = TileFactory(
            quote_id=QuoteFactory().pk,
            template_id=TemplateFactory().pk,
            image='test-english.jpg',
            english=True
        )

        self.payload['text'] += ' --english'

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(response['attachments'][0]['image_url'], 'http://testserver/{}'.format(tile.image))
        self.assertEqual(response['attachments'][0]['thumb_url'], 'http://testserver/{}'.format(tile.image))

        # Is always a space
        self.assertEqual(response['attachments'][0]['text'], ' ')

    def test_tile_and_image(self):
        """
        Test if two attachments are available. Attachment content is already tested in other tests.
        """

        quote = QuoteFactory(image='image.jpg')

        TileFactory(quote=quote, template=TemplateFactory(), image='tile.jpg')

        response = self.client.post('/api/', self.payload).json()

        self.assertEqual(len(response['attachments']), 2)
