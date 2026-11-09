# Rutas propias de la aplicación 'contact' (se incluyen desde evaluacion_2/urls.py)
# Importa path para definir cada ruta
from django.urls import path

# Importa las vistas de esta misma app
from . import views

# Lista de rutas de la app; Django la lee gracias a include('contact.urls') en el urls.py principal
urlpatterns = [
    # /contacto/ : muestra el formulario y guarda los mensajes enviados
    # '' significa "la raíz de esta app", que ya tiene el prefijo 'contacto/'; name='contacto' permite usar {% url 'contacto' %}
    path('', views.contacto, name='contacto'),
]
