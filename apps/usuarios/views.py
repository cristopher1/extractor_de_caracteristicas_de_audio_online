from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import get_user_model
from .models import *

Usuario = get_user_model()

# Create your views here.
class Registro(View):
    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url=reverse_lazy('caracteristicas')))
    def dispatch(self, *args, **kwargs):
        return super(Registro, self).dispatch(*args, **kwargs)
        
    def get(self, request):
        return render(request, 'registro.html')
    def post(self, request):
        try:
            post_data = request.POST
            email, password = post_data['email'], post_data['password']
            Usuario.objects.create_user(email=email, password=password)
            return redirect(reverse('login'))
        except ValidationError as e:
            print(e)
            return render(request, 'inicio.html')