"""
ASGI config for evaluacion_2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""
# Docstring que documenta el propósito del archivo y referencia la guía oficial de despliegue ASGI en Django

# Módulo estándar para interactuar con el sistema operativo y variables de entorno
import os

# Función utilitaria del núcleo de Django que inicializa la aplicación ASGI nativa
from django.core.asgi import get_asgi_application

# Define 'evaluacion_2.settings' como el módulo de configuración por defecto del proyecto,
# sin sobreescribir la variable de entorno si ya fue fijada en el sistema
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_2.settings')

# Instancia y expone el objeto ejecutable ASGI a nivel de módulo bajo el nombre 'application',
# el cual será llamado por el servidor web asíncrono (ej. uvicorn evaluacion_2.asgi:application)
application = get_asgi_application()
