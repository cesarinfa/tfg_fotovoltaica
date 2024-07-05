from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserData, UsuarioxInst
from instalaciones.models import Instalacion


class RegistrationForm(UserCreationForm):
    nombre = forms.CharField(max_length = 40)
    apellidos = forms.CharField(max_length = 80)
    empresa = forms.CharField(max_length = 50)
    cif = forms.CharField(max_length = 10)
    telefono = forms.IntegerField()
    email = forms.EmailField(max_length = 100)
    direccion = forms.CharField(max_length = 100)
    cp = forms.IntegerField()
    poblacion = forms.CharField(max_length = 50)
    provincia = forms.CharField(max_length = 30)


    class Meta:
        model = User
        fields = ['nombre','apellidos','empresa','cif','telefono','email','direccion','cp',
        'poblacion','provincia','username','password1','password2']
        labels = {'username':'Usuario','password1':'Contraseña','password2':'Repetir Contraseña','cif':'CIF','cp':'CP'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for num, value in self.Meta.labels.items():
            self[num].label = value
            self[num].help_text = None


class RestablecerPassForm(forms.Form):
    email = forms.EmailField(max_length = 100)

    class Meta:
        model = User
        fields = ['email']

class ActualizarPassForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1','password2']
        labels = {'password1': 'Contraseña', 'password2': 'Repetir Contraseña'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for num, value in self.Meta.labels.items():
            self[num].label = value
            self[num].help_text = None


class RegPropietarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=40)
    apellidos = forms.CharField(max_length=80)
    telefono = forms.IntegerField()
    email = forms.EmailField(max_length=100)
    direccion = forms.CharField(max_length=100)
    cp = forms.IntegerField()
    poblacion = forms.CharField(max_length=50)
    provincia = forms.CharField(max_length=30)
    coche_elec = forms.BooleanField()
    aero = forms.BooleanField()



    class Meta:
        model = User
        fields = ['nombre','apellidos','telefono','email','direccion','cp','poblacion','provincia','coche_elec','aero',
                  'username','password1','password2']
        labels = {'username':'Usuario','password1':'Contraseña','password2':'Repetir Contraseña','cp':'CP',
                  'aero':'Aerotermia','coche_elec':'Coche eléctrico'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for num, value in self.Meta.labels.items():
            self[num].label = value
            self[num].help_text = None


class LinkPropietarioForm(forms.Form):
     usuario = forms.Select()
     instalacion = forms.Select()

     class Meta:
        model = UsuarioxInst
        fields = ['usuario','instalacion']
