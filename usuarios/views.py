from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, RestablecerPassForm, ActualizarPassForm, RegPropietarioForm, LinkPropietarioForm
from .models import UserData, UsuarioxInst
from .token import account_activation_token
from instalaciones.models import Instalacion

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.auth.hashers import make_password


# Create your views here.

def p404(request):
    return render(request, 'admin/404.html', {})


def home(request):
    if request.method == "GET":
        return render(request, 'home.html', {'form': AuthenticationForm, })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'home.html', {'form': AuthenticationForm,
                                                 'error': 'Usuario o contraseña incorrecto'})
        else:
            login(request, user)
            return redirect('/instalaciones/insta')


def registro(request):
    if request.method == 'GET':
        return render(request, 'registros.html', {'form': RegistrationForm})

    else:

        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.is_active = False
            user.save()
            login(request, user)

            # Guardar la información de usuario

            userData = UserData()
            userData.user = User.objects.get(username=request.POST['username'])
            userData.nombre = request.POST['nombre']
            userData.apellidos = request.POST['apellidos']
            userData.empresa = request.POST['empresa']
            userData.cif = request.POST['cif']
            userData.telefono = request.POST['telefono']
            userData.email = request.POST['email']
            userData.direccion = request.POST['direccion']
            userData.cp = request.POST['cp']
            userData.poblacion = request.POST['poblacion']
            userData.provincia = request.POST['provincia']

            userData.save()

            # Enviar email de confirmación

            current_site = get_current_site(request)
            mail_subject = 'Enlace de activación de usuario'
            message = render_to_string('activar_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return render(request, 'usuario_creado.html',{'usuario': user})
        else:
            return render(request, 'registros.html', {'form': RegistrationForm,
                                                      'error': form.errors})


def activar(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'usuario_activado.html',{'confirm':True})
    else:
        return render(request, 'usuario_activado.html',{'confirm':False})


def password_reset(request):
    if request.method == 'GET':
        return render(request, 'password_reset.html', {'form': RestablecerPassForm})
    else:

        form = RestablecerPassForm(request.POST)

        if form.is_valid():

            userData = UserData.objects.filter(email=request.POST['email'])

            if userData:
                user = User.objects.get(id=userData[0].user_id)
                current_site = get_current_site(request)
                mail_subject = 'Enlace de restauración de contraseña'
                message = render_to_string('requerir_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()

                return render(request, 'password_enviada.html')
            else:
                return render(request, 'password_reset.html', {'form': RestablecerPassForm,
                                                               'error': 'No existe ningún usuario con ese email en nuestra base de datos'})

def restaurar(request, uidb64, token):
    if request.method == 'GET':
        return render(request, 'restaurar.html', {'form': ActualizarPassForm})

    else:
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if (password1 == password2):

            User = get_user_model()
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and account_activation_token.check_token(user, token):
                user.password = make_password(password1)
                user.save()
                return render(request, 'password_confirmada.html',{'confirm':True})
            else:
                return render(request, 'password_confirmada.html',{'confirm':False})
        else:
            return render(request, 'restaurar.html', {'form': ActualizarPassForm,
                                                      'error': 'Los campos no son iguales'})


@login_required
def info_usuarios(request):
    data_info = UserData.objects.filter(user=request.user)

    return render(request, 'usuario.html', {'info': data_info[0]})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('usuarios:home')






def reg_propietario(request):
    if request.method == 'GET':
        data_info = UserData.objects.filter(user=request.user)
        return render(request, 'reg_propietario.html', {'form': RegPropietarioForm,'info': data_info[0]})

    else:

        form = RegPropietarioForm(request.POST)

        instalador = request.user.id

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.is_active = False
            user.save()

            # Guardar la información de usuario



            userData = UserData()
            userData.user = User.objects.get(username=request.POST['username'])
            userData.nombre = request.POST['nombre']
            userData.apellidos = request.POST['apellidos']
            userData.telefono = request.POST['telefono']
            userData.email = request.POST['email']
            userData.direccion = request.POST['direccion']
            userData.cp = request.POST['cp']
            userData.poblacion = request.POST['poblacion']
            userData.provincia = request.POST['provincia']
            if request.POST['coche_elec'] == 'on':
                userData.coche_elec = True
            else:
                userData.coche_elec = False

            if request.POST['aero'] == 'on':
                userData.aero = True
            else:
                userData.aero = False

            userData.instalador =  instalador
            userData.save()


            # Enviar email de confirmación

            current_site = get_current_site(request)
            mail_subject = 'Enlace de activación de usuario'
            message = render_to_string('activar_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return render(request, 'usuario_creado.html', {'usuario': user})
        else:
            return render(request, 'registros.html', {'form': RegistrationForm,
                                                      'error': form.errors})


@login_required
def usuario_link(request):

    user_datas = UserData.objects.filter(instalador=request.user.id)
    instalaciones = Instalacion.objects.filter(user_id=request.user.id)
    usuarios = []

    for user_data in user_datas:
        user = { 'id': user_data.id, 'username': get_object_or_404(User,id=user_data.id)}
        usuarios.append(user)



    if request.method == 'GET':
        data_info = UserData.objects.filter(user=request.user)
        return render(request, 'usuario_link.html', {'form': LinkPropietarioForm,'info': data_info[0],
                                                     'usuarios':usuarios,'instalaciones':instalaciones})

    else:

        if request.POST['usuario'] != '' and request.POST['instalacion'] != '':
            userxinst = UsuarioxInst()
            userxinst.user_id= request.POST['usuario']
            userxinst.inst_id= request.POST['instalacion']

            try:
                userxinst.save()
            except:
                data_info = UserData.objects.filter(user=request.user)
                return render(request, 'usuario_link.html', {'form': LinkPropietarioForm, 'info': data_info[0],
                                                             'usuarios': usuarios, 'instalaciones': instalaciones,
                                                             'error': 'Ya está asignado ese usuario a la instalación'})

            return render(request, 'usuario_link.html', {'form': LinkPropietarioForm,
                                                          'success': 'Se ha añadido correctamente la instalación al usuario'})
        else:
            data_info = UserData.objects.filter(user=request.user)
            return render(request, 'usuario_link.html', {'form': LinkPropietarioForm,'info': data_info[0],
                                                         'usuarios':usuarios,'instalaciones':instalaciones,
                                                         'error':'Seleccione correctamente un usuario y una instalación'})

def usuario_creado(request):
    return redirect('usuario_creado.html')

def usuario_activado(request):
    return redirect('usuario_activado.html')

def password_enviada(request):
    return redirect('password_enviada.html')

def password_confirmada(request):
    return redirect('password_confirmada.html')
