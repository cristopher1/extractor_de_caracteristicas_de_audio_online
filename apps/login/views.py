from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse

Usuario = get_user_model()

# Create your views here.
class Login(View):
    @method_decorator(user_passes_test(lambda user: not user.is_authenticated, login_url=reverse_lazy('caracteristicas')))
    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        try:
            data_post = request.POST
            email, password = data_post['email'], data_post['password']
            #comprobar que los datos pasados por POST, coinciden con el modelo
            validate_user = Usuario(email=email, password=password)
            validate_user.clean_fields(['unique'])
            user = authenticate(email=email, password=password)
            if user is None:
                return render(request, 'inicio.html', context={'error': 'No esta registrado en la aplicación'})
            else:
                login(request, user)
                return redirect(reverse('caracteristicas'))
                
        except ValidationError as e:
            print(e)
            return render(request, 'inicio.html', context={'error': e})

class Logout(View):
    def get(self, request):
        logout(request)
        return render(request, 'inicio.html')