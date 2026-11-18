# Rutas propias de la app 'tienda' (se incluyen desde evaluacion_2/urls.py)
# Importa path para definir cada ruta
from django.urls import path

# Importa las vistas de esta misma app
from . import views

# Lista de rutas de la tienda
urlpatterns = [
    # Raíz del sitio (/): catálogo con filtro por etiquetas (?categoria=<slug>), orden y paginación
    path('', views.index, name='index'),

    # Endpoint POST para guardar una valoración; captura el id del producto desde la URL (ej: /producto/14/valorar/)
    path('producto/<int:producto_id>/valorar/', views.agregar_valoracion, name='agregar_valoracion'),

    # Galería con todos los productos (/gallery/)
    path('gallery/', views.gallery, name='gallery'),
]
