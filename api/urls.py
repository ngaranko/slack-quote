from django.conf.urls import url, patterns
import api.views

urlpatterns = [
    url(r'^$', api.views.APIView.as_view()),
]

