from django.conf.urls import url, include
from apps.descripcion.views import *

urlpatterns = [
    url(r'^descripcion/$', descripcion, name='descripcion'),
]