from django.conf.urls import url, include
from apps.inicio.views import *

urlpatterns = [
    url(r'^$', inicio, name='inicio'),
    url(r'^contacto/$', contacto, name='contacto'),
]