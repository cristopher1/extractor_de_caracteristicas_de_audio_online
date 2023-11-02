from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

def largo_contrasenna(value):
    min_elements = 5
    if len(value) < min_elements:
        Error = ValidationError(
            _('La contraseña tiene menos de %(n)s elementos'),
            code="Contraseña corta",
            params={'n': min_elements}
            )
        raise Error

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user
    
    def create_superuser(self, email, password):
        return self.create_user(email, password, admin=True, staff=True)

# Create your models here.
class Usuario(AbstractUser):
    email=models.EmailField(primary_key=True, unique=True, null=False, blank=False)
    password=models.CharField(max_length=97, validators=[largo_contrasenna])
    es_activo=models.BooleanField(default=True)
    admin=models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    username=None
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['password']
    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_active(self):
        return self.es_activo

    class Meta:
        db_table='usuario'