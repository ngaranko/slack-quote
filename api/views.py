from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

import quote.service as quote_service
from api.forms import SlackPOSTForm
from api.serializers import in_channel_response
from quote.models import Quote, Author


class APIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        form = SlackPOSTForm(data=request.POST)

        quote = None

        if not form.is_valid():
            return JsonResponse(data={}, status=400)

        cleaned_data = form.cleaned_data

        if cleaned_data.get('previous'):
            quote = quote_service.previous()

        if not quote:
            quote = quote_service.search(form.cleaned_data['text'])

        if not quote:
            quote = quote_service.next()

        if quote:
            quote_service.hit(quote=quote)
        else:
            quote = Quote(text='No quote in database', author=Author(name='System message'))

        prefix = 'https://' if request.is_secure() else 'http://'
        path = prefix + request.get_host() + '/'
        english = cleaned_data.get('english')

        return JsonResponse(in_channel_response(quote=quote, path=path, english=english))
