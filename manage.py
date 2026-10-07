#!/usr/bin/env python
# Shebang: indica a los sistemas Unix/Linux/macOS con qué intérprete ejecutar este script si se invoca directamente (./manage.py)

"""Django's command-line utility for administrative tasks."""
# Docstring de módulo: describe brevemente el propósito del archivo

# Módulo estándar para interactuar con variables de entorno y el sistema operativo
import os

# Módulo estándar para acceder a parámetros del sistema, incluidos los argumentos pasados por consola (sys.argv)
import sys


def main():
    """Run administrative tasks."""
    # Función principal encargada de configurar el entorno y ejecutar la orden solicitada

    # Apunta la variable de entorno 'DJANGO_SETTINGS_MODULE' al archivo de configuración de este proyecto ('evaluacion_2.settings')
    # setdefault asegura no sobreescribir la variable si ya fue definida manualmente en la consola
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion_2.settings')
    
    try:
        # Intenta importar la función que procesa y despacha los comandos de gestión en Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o el entorno virtual (.venv) no está activo, lanza un error claro y detallado
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ejecuta el comando de Django pasando la lista de argumentos recibidos en la terminal (ej: ['manage.py', 'runserver'])
    execute_from_command_line(sys.argv)


# Comprueba si el script se está ejecutando directamente como programa principal (no importado como módulo)
if __name__ == '__main__':
    # Invoca la función principal para comenzar la ejecución
    main()
