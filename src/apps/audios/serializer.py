from rest_framework import serializers
from apps.audios.models import *

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'