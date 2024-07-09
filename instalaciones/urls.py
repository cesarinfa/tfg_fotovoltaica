from django.urls import path
from . import views as instalaciones_views


urlpatterns = [
    path('insta/', instalaciones_views.instalaciones, name='instalaciones'),
    path('<int:insta_id>/info_consumos',instalaciones_views.info_instalacion,name='info_consumos'),
    path('<int:insta_id>/prev_meteorologica',instalaciones_views.prev_meteoro,name='prev_meteorologica'),
    path('<int:insta_id>/prev_energia',instalaciones_views.prev_energia,name='prev_energia'),
    path('nueva_instalacion/',instalaciones_views.nueva_instalacion,name='nueva_instalacion'),
]