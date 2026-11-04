# Importa la clase base AppConfig desde el módulo de aplicaciones de Django
from django.apps import AppConfig


# Define la clase de configuración específica para la aplicación 'errores', heredando de AppConfig
class ErroresConfig(AppConfig):
    # Especifica la ruta de importación de Python para la aplicación (nombre del módulo/paquete)
    name = 'errores'
    # Nombre legible de la aplicación
    verbose_name = 'Páginas de error'
