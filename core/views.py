# Vistas de la app 'core': solo las páginas generales del sitio (Quiénes somos y Preguntas frecuentes)
# Todo lo operativo de la tienda (catálogo, filtros, valoraciones, galería) está en la app 'tienda'

# render: dibuja una plantilla HTML y la devuelve como respuesta
from django.shortcuts import render


# Vista de la página "Quiénes somos" (URL /about/)
def about(request):
    """Renderiza la sección informativa 'Quiénes somos'."""
    # Dibuja la plantilla sin enviar datos extra (las categorías llegan por el procesador de contexto)
    return render(request, 'core/about.html')


# Vista de preguntas frecuentes (URL /faq/)
def faq(request):
    """Renderiza la página de preguntas frecuentes."""
    # Dibuja la plantilla de preguntas frecuentes
    return render(request, 'core/faq.html')
