# Rutas propias de la app 'core' (páginas generales del sitio; se incluyen desde evaluacion_2/urls.py)
# Importa path para definir cada ruta
from django.urls import path

# Importa las vistas de esta misma app
from . import views

# Lista de rutas de las páginas generales
urlpatterns = [
    # Página "Quiénes somos" (/about/)
    path('about/', views.about, name='about'),

    # Preguntas frecuentes (/faq/)
    path('faq/', views.faq, name='faq'),
]
