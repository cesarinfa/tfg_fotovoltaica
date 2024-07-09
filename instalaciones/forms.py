from .models import Instalacion
from django import forms

# Formulario de registro de instalación
class InstalacionForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=100)
    cp = forms.IntegerField()
    poblacion = forms.CharField(max_length=50)
    provincia = forms.CharField(max_length=30)
    latitud = forms.DecimalField(max_digits=9, decimal_places=6)
    longitud = forms.DecimalField(max_digits=9, decimal_places=6)
    fecha_inst = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"])
    modelo_inv = forms.CharField(max_length=30)
    fabricante_inv = forms.CharField(max_length=30)
    nserie_inv = forms.CharField(max_length=30)

    # Campos a mostrar
    class Meta:
        model = Instalacion
        fields = ['nombre','direccion','cp','poblacion','provincia','latitud','longitud','fecha_inst', 'modelo_inv',
                  'fabricante_inv', 'nserie_inv']


# Formulario para históricos
class HistoricoForm(forms.Form):
    desde = forms.DateField(widget = forms.SelectDateWidget)
    hasta = forms.DateField(widget = forms.SelectDateWidget)
