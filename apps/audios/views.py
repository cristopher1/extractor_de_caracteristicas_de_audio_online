from apps.audios.serializer import AudioSerializer
from apps.audios.forms import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

def generar_data(request):
    usuario = request.user
    archivo = request.FILES['audio']
    nombre = archivo.name
    return dict(usuario=usuario, archivo=archivo, nombre=nombre)

def serializer_model(serializer):
    return serializer.Meta.model

# Create your views here.

#Utilizado para responder a peticiones POST y PUT asociadas al recurso audio de un usuario
class AudioAPI(APIView):
    def post(self, request):
        try:
            audio_data = generar_data(request)
            audio_usuario = audio_data['usuario']
            audio_nombre = audio_data['nombre']
            serializer_model(AudioSerializer).objects.get(nombre=audio_nombre, usuario=audio_usuario)
            return Response(status=status.HTTP_409_CONFLICT)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except serializer_model(AudioSerializer).DoesNotExist:
            serialize = AudioSerializer(data=audio_data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            audio_data = generar_data(request)
            audio_usuario, audio_archivo, audio_nombre = audio_data.values()
            audio = serializer_model(AudioSerializer).objects.get(nombre=audio_nombre, usuario=audio_usuario)
            serialize = AudioSerializer(audio, data={'archivo': audio_archivo}, partial=True)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return Response(status=status.HTTP_200_OK)         
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except serializer_model(AudioSerializer).DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)            
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AudioPagination(PageNumberPagination):
    page_size=30000
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

#Utilizado para obtener los recursos audios de un determinado usuario, mediante paginación
class AudioListAPIView(ListAPIView):
    serializer_class=AudioSerializer
    pagination_class = AudioPagination
    model = serializer_model(AudioSerializer)
    def get_queryset(self):
        usuario =self.request.user
        audios = self.model.objects.filter(usuario=usuario).order_by('-fecha')
        return audios
