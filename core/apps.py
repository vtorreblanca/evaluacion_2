# Importa la clase base AppConfig desde el módulo de aplicaciones de Django
from django.apps import AppConfig


# Define la clase de configuración específica para la aplicación 'core', heredando de AppConfig
class CoreConfig(AppConfig):
    # Especifica la ruta de importación de Python para la aplicación (nombre del módulo/paquete)
    name = 'core'

