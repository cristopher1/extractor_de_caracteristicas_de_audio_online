from django import forms
from apps.audios.models import *

class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields=['usuario', 'nombre', 'archivo']
        
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)