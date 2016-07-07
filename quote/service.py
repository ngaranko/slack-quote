from django.db.models import Q, F
from django.utils import timezone
from quote.models import Author, Quote


def search(keyword_string):

    keywords = keyword_string.split(' ')

    queries = [Q(author__name__icontains=keyword) for keyword in keywords if keyword.strip()]
    queries += [Q(text__icontains=keyword) for keyword in keywords if keyword.strip()]

    query = queries.pop()

    for item in queries:
        query |= item

    return Quote.objects.filter(query).order_by('-last_hit', '-author__last_hit').first()

def hit(quote):

    Author.objects.filter(pk=quote.author_id).update(hit_count=F("hit_count") + 1, last_hit=timezone.now())
    Quote.objects.filter(pk=quote.pk).update(hit_count=F("hit_count") + 1, last_hit=timezone.now())

def next():
    return Quote.objects.order_by('-last_hit', '-author__last_hit').first()