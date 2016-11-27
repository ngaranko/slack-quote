import factory

from tile.models import Template, Tile


class TemplateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Template


class TileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tile

    template = factory.SubFactory('tile.factories.TemplateFactory')
    quote = factory.SubFactory('quote.factories.QuoteFactory')
