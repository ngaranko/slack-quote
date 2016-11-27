from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import quote.service as quote_service
from api.forms import SlackPOSTForm
from api.serializers import in_channel_response
from quote.models import Quote


class APIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = SlackPOSTForm(data=request.POST)

        quote = None

        if form.is_valid():
            quote = quote_service.search(form.cleaned_data['text'])

        if not quote:
            quote = quote_service.next()

        if quote:
            quote_service.hit(quote=quote)
        else:
            quote = Quote(text='No quote in database')

        prefix = 'https://' if request.is_secure() else 'http://'
        path = prefix + request.get_host() + '/'

        return JsonResponse(in_channel_response(quote=quote, path=path))
