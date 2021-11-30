from django.shortcuts import render
from django.views.generic import View
from apps.audios.models import *
from apps.caracteristicas.forms import *
from project.settings import MEDIA_ROOT
from .extraccionCaracteristicas.backend import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

def generar_data(data):
    kwargs = {}
    data = data.cleaned_data
    for clave in ['n_fft', 'hop_length', 'n_mfcc', 'dct_type']:
        valor = data.get(clave)
        if valor:
            kwargs[clave] = valor
    return kwargs

#indice 0: formulario, indice 1: titulo
Info = {
    'amplitud': (SerieTiempoAmplitudForm, "Serie de tiempo de la amplitud"),
    'espectrograma': (EspectrogramaTradicionalForm, "Espectrograma"),
    'espectrograma_mel': (EspectrogramaMelForm, "Espectrograma de MEL"),
    'mfcc_mel': (MfccEspectrogramaMelForm, "{0} MFCCs (Generado a partir del espectrograma MEL)"),
    'mfcc_amplitud': (MfccAmplitudForm, "{0} MFCCs (Generado a partir de la serie de tiempo de amplitud)"),
}

# Create your views here.
class Caracteristica(View):
    def get(self, request):
        context = {
            "form_audio": AudioForm,
            "form_espectrograma_tradicional": EspectrogramaTradicionalForm,
            "form_espectrograma_mel": EspectrogramaMelForm,
            "form_serie_tiempo_amplitud": SerieTiempoAmplitudForm,
            "form_mfcc_amplitud": MfccAmplitudForm,
            "form_mfcc_mel": MfccEspectrogramaMelForm
        }
        return render(request, 'generar_caracteristica.html', context=context)

class CaracteristicaAPI(APIView):
    def post(self, request):
        try:
            usuario = request.user
            tipo = request.POST['tipo']
            form, titulo = Info[tipo]
            form = form(request.POST)
            if form.is_valid() and Audio.objects.get(nombre=form['audio'].value(), usuario=usuario):
                ruta_audio = MEDIA_ROOT / usuario.get_username() / form['audio'].value()
                tasa_muestreo = int(form['tasa_muestreo'].value())
                kwargs = generar_data(form)
                audio = cargar_audio(ruta_audio, tasa_muestreo)
                caracteristica = None
                if tipo == 'amplitud':
                    caracteristica = Amplitud(audio)
                elif tipo == 'espectrograma':
                    caracteristica = EspectrogramaTradicional(audio, **kwargs)
                elif tipo == 'espectrograma_mel':
                    caracteristica = EspectrogramaMEL(audio, **kwargs)
                elif tipo == 'mfcc_mel':
                    espect_mel = EspectrogramaMEL(audio, n_fft = kwargs['n_fft'], hop_length=kwargs['hop_length'])
                    caracteristica = MFCCEspectrogramaMEL(espect_mel, n_mfcc=kwargs['n_mfcc'], dct_type=kwargs['dct_type'])
                elif tipo == 'mfcc_amplitud':
                    ampl = Amplitud(audio)
                    caracteristica = MFCCAmplitud(ampl, **kwargs)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                data_response = {
                    'png': caracteristica.generar_png(titulo),
                    'pickle': caracteristica.generar_pickle(),
                }
                return Response(data_response, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Audio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
