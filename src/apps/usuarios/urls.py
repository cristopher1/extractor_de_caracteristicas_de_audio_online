from django.conf.urls import url, include
from apps.usuarios.views import *

urlpatterns = [
    url(r'^registro/$', Registro.as_view(), name='registro'),
]