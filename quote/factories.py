import factory


from quote.models import Quote, Author


class QuoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Quote

    author = factory.SubFactory('quote.factories.AuthorFactory')


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
