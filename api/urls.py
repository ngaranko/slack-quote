from django.conf.urls import url

import api.views

urlpatterns = [
    url(r'^$', api.views.APIView.as_view()),
]

