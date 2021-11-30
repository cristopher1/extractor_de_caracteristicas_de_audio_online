import json
import os
from django.shortcuts import render
from pathlib import Path
from enum import Enum
from math import ceil

class Info:
    class Caracteristica (Enum):
        todas = 0
    class Aplicacion(Enum):
        descripcion = 0
    @staticmethod
    def obtenerInformacion(ruta):
        URL_BASE = Path(__file__).resolve().parent
        info = None
        with open(os.path.join(URL_BASE, 'json', ruta), encoding='utf-8') as archivo:
            info = json.load(archivo)
        return info
    @staticmethod
    def formatearDescripcion(data):
        try:
            clave = 'descripcion'
            for info in data:
                info[clave] = ' '.join(info[clave])
        except:
            pass

def generarRuta(*args, extension='json'):
    return os.path.join(*args) + '.' + extension

# Create your views here.
def descripcion(request):
    ruta = generarRuta('info_app', Info.Aplicacion.descripcion.name)
    info_app = Info.obtenerInformacion(ruta)
    for seccion in info_app['secciones']:
        Info.formatearDescripcion(seccion['info'])
    context = dict(data = info_app)
    return render(request, 'descripcion.html', context)