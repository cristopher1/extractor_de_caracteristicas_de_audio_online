from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls.base import reverse_lazy

# Create your views here.
@user_passes_test(lambda user: not user.is_authenticated, login_url=reverse_lazy('caracteristicas'))
def inicio(request):
    return render(request, 'inicio.html')

def contacto(request):
    return render(request, 'contacto.html')