import factory

from tile.models import Template, Tile


class TemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Template


class TileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tile

    template = factory.RelatedFactory('tile.factories.TemplateFactory')
    quote = factory.RelatedFactory('quote.factories.QuoteFactory')
