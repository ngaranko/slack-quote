from django.core.management import BaseCommand
from django.core.management import CommandError

from quote.models import Quote
from tile.models import Template

import tile.service as tile_service


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Overwrites all tiles',
        )

    def handle(self, *args, **options):

        try:
            template = Template.objects.get(is_default=True)
        except Template.MultipleObjectsReturned:
            raise CommandError('There is more than one default template configured. Only one is allowed')
        except Template.DoesNotExist:
            raise CommandError('No default template found')

        if options['force']:
            quotes = Quote.objects.all()
        else:
            quotes = Quote.objects.filter(tile__id=None)

        for quote in quotes:

            if quote.tile.exists():
                quote.tile.all().delete()

            tile_service.create(quote=quote, template=template)
            self.stdout.write('Created tile for quote {}'.format(quote.id))
