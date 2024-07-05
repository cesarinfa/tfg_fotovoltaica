from django.db import models
from django.contrib.auth.models import User
from instalaciones.models import Instalacion

# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 40)
    apellidos = models.CharField(max_length=80)
    instalador = models.IntegerField(default=0)
    empresa = models.CharField(max_length=50,default='')
    cif = models.CharField(max_length=10,default='')
    coche_elec = models.BooleanField(default=False)
    aero = models.BooleanField(default=False)
    telefono = models.PositiveIntegerField(null=True)
    email = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100,default='')
    cp = models.PositiveIntegerField(null=True)
    poblacion = models.CharField(max_length=50,default='')
    provincia = models.CharField(max_length=30,default='')


class UsuarioxInst(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
        inst = models.ForeignKey(Instalacion, on_delete=models.CASCADE, null=False, blank=False)

        class Meta:
            unique_together = ('user', 'inst',)

