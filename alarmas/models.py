from django.db import models
from instalaciones.models import Instalacion

# Create your models here.



class Alarmas(models.Model):

    ESTADOS = (('ACTIVA','ACTIVA'),('SOLUCIONADA','SOLUCIONADA'))
    TIPOS = (('LEVE','LEVE'),('INTERMEDIA','INTERMEDIA'),('CRÍTICA','CRÍTICA'))

    fecha = models.DateTimeField()
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE, null=False, blank=False)
    estado = models.CharField(max_length=20,null=False,choices=ESTADOS)
    tipo = models.CharField(max_length=20,null=False,choices=TIPOS)
    descripcion = models.CharField(max_length=250)