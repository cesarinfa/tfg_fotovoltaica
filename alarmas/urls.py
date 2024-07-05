from django.urls import path, include
from . import views as alarmas_views


urlpatterns = [
    path('listado/', alarmas_views.alarmas, name='alarmas'),
]