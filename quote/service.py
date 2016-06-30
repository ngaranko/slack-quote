from django.db.models import Q
from quote.models import Author, Quote


def search(keyword_string):

    keywords = keyword_string.split(' ')

    queries = [Q(author__name__icontains=keyword) for keyword in keywords if keyword.strip()]
    queries += [Q(text__icontains=keyword) for keyword in keywords if keyword.strip()]

    query = queries.pop()

    for item in queries:
        query |= item

    return Quote.objects.filter(query).order_by('hit_count', 'author__hit_count').first()

def hit(quote):

    quote.author.hit_count +=1
    quote.author.save()
    quote.hit_count += 1
    quote.save()

def next():
    return Quote.objects.order_by('hit_count', 'author__hit_count').first()