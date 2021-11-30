import io
import base64
import pickle
import librosa
import librosa.display as display
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from abc import abstractmethod

def cargar_audio(ruta, sr):
  return librosa.load(ruta, sr)

#Clase base caracteristicas
class Caracteristica:
  def __init__(self, audio):
    self.data, self.tasaMuestreo = audio
  
  def obtenerAudio(self):
    return self.data, self.tasaMuestreo

  def obtenerTasaMuestreo(self):
    return self.tasaMuestreo

  def extraer(self):
    return self.caracteristica
  
  def generar_png(self, titulo):
    fig = self.graficar(titulo)
    memory = io.BytesIO()
    
    plt.savefig(memory, format='png')
    plt.close(fig)

    png = memory.getvalue()
    memory.close()

    return base64.b64encode(png)    

  @abstractmethod
  def graficar(self, **kwargs):
    pass

  def generar_pickle(self):
    data = {
      'tasa_muestreo': self.obtenerTasaMuestreo(),
      'data': self.extraer(),
    }
    return base64.b64encode(pickle.dumps(data))

#Clase amplitud
class Amplitud(Caracteristica):
  def __init__(self, audio):
    super().__init__(audio)
    data, _ = self.obtenerAudio()
    self.caracteristica = data
  
  def graficar(self, title):
    caracteristica = self.extraer()
    tasaMuestreo = self.obtenerTasaMuestreo()

    fig = plt.figure()
    display.waveplot(caracteristica, tasaMuestreo, x_axis='s')
    plt.ylabel("Amplitud")
    plt.title(title)
    return fig

  def generar_pickle(self):
    pass    

#Clase espectrogramas
class Espectrograma(Caracteristica):
  def __init__(self, audio, function):
    super().__init__(audio)
    data, tasaMuestreo = self.obtenerAudio()
    self.caracteristica = librosa.amplitude_to_db(function(data, tasaMuestreo), ref=np.max)
  
  def graficar(self, **kwargs):
    caracteristica = self.extraer()
    tasaMuestreo = self.obtenerTasaMuestreo()
    title = kwargs['title']
    del kwargs['title']

    fig = plt.figure()
    display.specshow(caracteristica, sr=tasaMuestreo, **kwargs)
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    return fig

class EspectrogramaTradicional(Espectrograma):
  def __init__(self, audio, **kwargs):
    super().__init__(audio, lambda y, sr: np.abs(librosa.stft(y=y, **kwargs)))

  def graficar(self, title):
    super().graficar(x_axis='s', y_axis='log', title=title)

class EspectrogramaMEL(Espectrograma):
  def __init__(self, audio, **kwargs):
    super().__init__(audio, lambda y, sr: librosa.feature.melspectrogram(y=y, sr=sr, **kwargs))
  
  def graficar(self, title):
    super().graficar(x_axis='s', y_axis='mel', title=title)

#Clase coeficientes cepstrales de la frecuencia de MEL
class MFCC(Caracteristica):
  def __init__(self, audio, n_mfcc, function):
    super().__init__(audio)
    data, tasaMuestreo = self.obtenerAudio()
    self.caracteristica = function(data, tasaMuestreo)
    self.n_mfcc = n_mfcc
  
  def graficar(self, **kwargs):
    caracteristica = self.extraer()
    title = kwargs['title']
    del kwargs['title']
    plt.imshow(caracteristica, **kwargs)
    plt.colorbar()
    plt.xlabel("N° Muestra")
    plt.ylabel("Coeficientes ceptrales de mel")
    plt.title(title.format(self.n_mfcc))

class MFCCAmplitud(MFCC):
  def __init__(self, amplitud, **kwargs):
    audio = amplitud.extraer(), amplitud.obtenerTasaMuestreo()
    super().__init__(audio, kwargs['n_mfcc'], lambda y, sr: librosa.feature.mfcc(y=y, sr=sr, **kwargs))

  def graficar(self, title):
    super().graficar(cmap=plt.cm.jet, aspect='auto',origin='lower', title=title)

class MFCCEspectrogramaMEL(MFCC):
  def __init__(self, espectrograma, **kwargs):
    audio = espectrograma.extraer(), espectrograma.obtenerTasaMuestreo()
    super().__init__(audio, kwargs['n_mfcc'], lambda S, sr: librosa.feature.mfcc(S=S, **kwargs))

  def graficar(self, title):
    super().graficar(cmap=plt.cm.jet, aspect='auto',origin='lower', title=title)
