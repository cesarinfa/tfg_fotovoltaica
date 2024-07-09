from django.db import models
from django.contrib.auth.models import User

# Modelo Instalación
class Instalacion(models.Model):
    nombre = models.CharField(max_length=50, default=None)
    direccion = models.CharField(max_length=100)
    cp = models.PositiveIntegerField()
    poblacion = models.CharField(max_length=50)
    provincia = models.CharField(max_length=30)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    fecha_inst = models.DateField()
    modelo_inv = models.CharField(max_length=30)
    fabricante_inv = models.CharField(max_length=30)
    nserie_inv = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='instalaciones')

    def __str__(self):
        return self.nombre


# Modelo Valores_Actual
class Valores_Actuales(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    consumida = models.DecimalField(max_digits=6, decimal_places=1)
    generada = models.DecimalField(max_digits=6, decimal_places=1)

    # función que devuelve lo emitido o consumido de la red eléctrica
    def red_electrica(self):
        return (self.consumida - self.generada)


# Modelo Histórico por hora
class Historico_Hora(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    hora = models.DateTimeField()
    consumida = models.DecimalField(max_digits=6, decimal_places=1)
    generada = models.DecimalField(max_digits=6, decimal_places=1)


# Modelo Histórico por día
class Historico_Dia(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    dia = models.DateField()
    consumida = models.DecimalField(max_digits=6, decimal_places=1)
    generada = models.DecimalField(max_digits=6, decimal_places=1)


# Modelo Histórico por mes
class Historico_Mes(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    mes = models.IntegerField()
    year = models.IntegerField()
    consumida = models.DecimalField(max_digits=6, decimal_places=1)
    generada = models.DecimalField(max_digits=6, decimal_places=1)

