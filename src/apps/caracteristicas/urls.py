from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from apps.caracteristicas.views import *

urlpatterns = [
    url(r'^caracteristicas/$', login_required(Caracteristica.as_view(), login_url=reverse_lazy('login')), name='caracteristicas'),
]

urlapi = [
    url(r'api/v1/caracteristicas/$', CaracteristicaAPI.as_view(), name='api_caracteristicas'),
]

urlpatterns += urlapi