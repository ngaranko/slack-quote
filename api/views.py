from api.forms import SlackPOSTForm
from api.serializers import in_channel_response
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, View

import quote.service as quote_service

class APIView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # <view logic>
        return HttpResponse('result')


    def post(self, request):

        form = SlackPOSTForm(data=request.POST)

        quote = None

        if form.is_valid():
            quote = quote_service.search(form.cleaned_data['text'])

        if not quote:
            quote = quote_service.next()

        quote_service.hit(quote=quote)

        return JsonResponse(in_channel_response(text=str(quote),sub_text=quote.context))