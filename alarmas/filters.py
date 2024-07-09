import django_filters
from django_filters import DateFilter
from django import forms

from instalaciones.models import Instalacion
from .models import Alarmas

# Función para fechas
class DateInput(forms.DateInput):
    input_type = 'date'


# Función que devuelve las instalaciones del usuario para el formulario
def buscar_instalaciones_usuario(request):
    if request is None:
        return Instalacion.objects.all()

    return Instalacion.objects.filter(user_id=request.user.id)


# Filtro para mostrar en la página de alarmas
class AlarmasFilter(django_filters.FilterSet):

    # Fechas de inicio y fin y comprueba instalaciones del usuario
    fecha_inicio = DateFilter(field_name='fecha',lookup_expr='gte',widget=DateInput(attrs={'type': 'date'}),label='Fecha inicio')
    fecha_final = DateFilter(field_name='fecha',lookup_expr='lte',widget=DateInput(attrs={'type': 'date'}),label='Fecha fin')
    instalacion = django_filters.ModelChoiceFilter(queryset=buscar_instalaciones_usuario)

    # Excluye fecha y descripción
    class Meta:
        model = Alarmas
        exclude = ['fecha','descripcion']