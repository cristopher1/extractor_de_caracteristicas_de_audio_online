# El modulo librosa procesa audio usando las librerías audioread y soundfile. Si se quiere
# procesar archivos .mp3 mediante librosa, se tendrá que instalar paquetes adicionales para
# que audioread pueda hacerlo, para ello puede consultar la página
# https://github.com/beetbox/audioread
FROM python:3.8 as base

# Se instalan paquetes necesarios para que las bibliotecas usadas por librosa puedan
# procesar audio.
RUN apt-get update && apt-get install -y \
    # Necesario para que funcione correctamente soundfile. Soundfile puede
    # procesar archivos .wav usando libsndfile
    libsndfile1-dev \
    # Necesario para que funcione correctamente audioread. Audioread puede
    # procesar archivos .mp3 usando ffmpeg mediante la interfaz de comandos
    ffmpeg

# Se establece el directorio de trabajo actual
WORKDIR /usr/src/api

FROM base as development

# Se instalan paquetes que solamente se usarán en el entorno de desarrollo
RUN apt-get update && apt-get install -y \
    # editor de texto
    nano \
    # pip, para instalar dependencias
    python3-pip

# Se copia el archivo con las dependencias
COPY requirements.dev.txt ./

# Se instalan las dependencias
RUN pip --no-cache-dir install -r requirements.dev.txt

# Se copia el resto de los archivos a la carpeta de trabajo actual
COPY . ./

# Se expone el puerto
EXPOSE 3000

# Ejecutar de forma automática tareas asociadas con el entorno de desarrollo
ENTRYPOINT [ "./docker-entrypoint.sh" ]

# Se ejecuta la api
CMD [ "python", "manage.py", "runserver", "0.0.0.0:3000" ]

FROM base as production

# Se copia el archivo con las dependencias
COPY requirements.prod.txt ./

# Se instalan las dependencias
RUN pip --no-cache-dir install -r requirements.prod.txt

# Se copia el resto de los archivos a la carpeta de trabajo actual
COPY . ./

# Se expone el puerto
EXPOSE 443

# Se ejecuta la api
CMD [ "gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:443" ]