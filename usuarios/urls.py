from django.urls import path, include
from . import views as usuarios_views

app_name = 'usuarios'

urlpatterns = [
    path('404/', usuarios_views.p404),
    path('', usuarios_views.home, name='home'),
    path('registros/', usuarios_views.registro, name='registro'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         usuarios_views.activar, name='activar'),
    path('usuario/', usuarios_views.info_usuarios, name='usuario'),
    path('cerrar_sesion/', usuarios_views.cerrar_sesion, name='cerrar_sesion'),
    path('password_reset/', usuarios_views.password_reset, name='password_reset'),
    path('restaurar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         usuarios_views.restaurar, name='restaurar'),
    path('reg_propietario', usuarios_views.reg_propietario, name='reg_propietario'),
    path('usuario_link', usuarios_views.usuario_link, name='usuario_link'),
    path('usuario_creado', usuarios_views.usuario_creado, name='usuario_creado'),
    path('usuario_activado', usuarios_views.usuario_activado, name='usuario_activado'),
    path('password_enviada', usuarios_views.password_enviada, name='password_enviada'),
    path('password_confirmada', usuarios_views.password_confirmada, name='password_confirmada'),

]