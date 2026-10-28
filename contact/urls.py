# Rutas propias de la aplicación 'contact' (se incluyen desde evaluacion_2/urls.py)
from django.urls import path

from . import views

urlpatterns = [
    # /contacto/ : muestra el formulario y guarda los mensajes enviados
    path('', views.contacto, name='contacto'),
]
