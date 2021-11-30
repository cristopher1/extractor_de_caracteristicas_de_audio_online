from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

Usuario = settings.AUTH_USER_MODEL

def ruta_archivo(instance, filename):
    return '{0}/{1}'.format(instance.usuario.email, filename)

class OverWriteStorage(FileSystemStorage):
    def _save(self, name, content):
        nombre_archivo = '{0}\{1}'.format(name.split('\\')[0], content.name)
        if self.exists(nombre_archivo):
            self.delete(nombre_archivo)
        return super(OverWriteStorage, self)._save(nombre_archivo, content)
    
# Create your models here.
class Audio(models.Model):
    class Meta:
        unique_together=[['usuario', 'nombre'],]

    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=200)
    archivo=models.FileField(upload_to=ruta_archivo, storage=OverWriteStorage())
    fecha=models.DateTimeField(auto_now=True)