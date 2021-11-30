from django import forms
from django.core import validators
from django.core.validators import MinValueValidator
from apps.audios.forms import *
# Create your models here.
class CaracteristicaForm(forms.Form):
    tasa_muestreo = forms.IntegerField(validators=[MinValueValidator], min_value=0)
    audio = forms.CharField()

class EspectrogramaForm(CaracteristicaForm):
    n_fft=forms.IntegerField(validators=[MinValueValidator], min_value=0)
    hop_length=forms.IntegerField(validators=[MinValueValidator], min_value=0)

class EspectrogramaTradicionalForm(EspectrogramaForm):
    pass

class EspectrogramaMelForm(EspectrogramaForm):
    pass

class SerieTiempoAmplitudForm(CaracteristicaForm):
    pass

class MfccAmplitudForm(CaracteristicaForm):
    n_mfcc=forms.IntegerField(validators=[MinValueValidator], min_value=1)
    dct_type=forms.IntegerField()

class MfccEspectrogramaMelForm(EspectrogramaForm):
    n_mfcc=forms.IntegerField(validators=[MinValueValidator], min_value=1)
    dct_type=forms.IntegerField()