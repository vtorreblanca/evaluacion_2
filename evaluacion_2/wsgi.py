"""
WSGI config for evaluacion_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""
# Docstring que describe el rol del archivo y referencia la documentación técnica de despliegue en Django

# Módulo estándar para manipular variables de entorno y recursos del sistema operativo
import os

# Función central de Django que inicializa el manejador WSGI y carga la configuración
from django.core.wsgi import get_wsgi_application

# Define 'evaluacion_2.settings' como la ruta del archivo de configuración por defecto
# setdefault garantiza no sobreescribir la variable si ya fue establecida previamente en el entorno del servidor
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_2.settings')

# Instancia y expone el objeto invocable (callable) WSGI a nivel de módulo con el identificador 'application'
# Este objeto es el que los servidores web de producción (Gunicorn, uWSGI, mod_wsgi) llaman para despachar solicitudes HTTP
application = get_wsgi_application()
