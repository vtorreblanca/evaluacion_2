# Importa la clase base AppConfig desde el módulo de aplicaciones de Django
from django.apps import AppConfig


# Configuración de la app 'tienda': contiene todo lo operativo de la tienda
# (modelos Categoria, Producto y Valoracion, su admin, el catálogo con filtros y el procesador de contexto)
class TiendaConfig(AppConfig):
    # Ruta de importación de la app (nombre de la carpeta)
    name = 'tienda'
    # Nombre legible que se muestra como título de la sección en el admin
    verbose_name = 'Tienda'
