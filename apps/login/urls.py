from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from apps.login.views import *

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', login_required(Logout.as_view(), login_url=reverse_lazy('login')), name='logout'),
]