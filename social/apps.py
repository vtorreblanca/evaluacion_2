# Importa la clase base AppConfig desde el módulo de aplicaciones de Django
from django.apps import AppConfig


# Define la clase de configuración específica para la aplicación 'social', heredando de AppConfig
class SocialConfig(AppConfig):
    # Especifica la ruta de importación de Python para la aplicación (nombre del módulo/paquete)
    name = 'social'
    # Nombre legible que se muestra en el panel de administración
    verbose_name = 'Redes sociales'
