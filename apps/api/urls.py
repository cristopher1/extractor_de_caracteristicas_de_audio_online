from django.conf.urls import url
from .views import *

#url app
urlpatterns = []

#url api
urlapi = [
    url(r'^v1/audio$', AudioAPI.as_view(), name='api_audios'),
    url(r'^v1/audios$', AudioListAPIView.as_view(), name='list_api_view_audios'),
]

urlpatterns += urlapi