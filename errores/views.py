# Importa render para dibujar una plantilla HTML y devolverla como respuesta
from django.shortcuts import render


# Mensaje que se muestra cuando el error no trae uno propio
MENSAJE_POR_DEFECTO = 'La página que buscas no existe.'


def pagina_404(request, exception=None):
    """
    Página común de error 404 para todo el sitio.
    - Django la usa como handler404 (registrado en evaluacion_2/urls.py) cuando DEBUG = False.
    - El middleware de esta app (errores/middleware.py) la usa cuando DEBUG = True.
    - Si la vista lanzó raise Http404('mensaje'), se muestra ese mensaje.
    """
    # Parte con el mensaje genérico
    mensaje = MENSAJE_POR_DEFECTO

    # Si llegó una excepción y su primer argumento es un texto, se usa como mensaje
    if exception is not None and exception.args and isinstance(exception.args[0], str):
        # Toma el texto con el que se lanzó el Http404
        texto = exception.args[0]
        # Los mensajes automáticos de Django vienen en inglés ("No X matches the given query."); esos no se muestran
        if 'matches the given query' not in texto:
            mensaje = texto

    # Renderiza la plantilla común de error
    respuesta = render(request, 'errores/404.html', {
        # Mensaje explicando qué no se encontró
        'mensaje': mensaje,
        # Ruta que pidió el usuario (ej: /productos/xyz/), para mostrarla en la página
        'ruta': request.get_full_path(),
    }, status=404)  # status=404: el navegador recibe el código HTTP 404 (no encontrado)

    # Marca la respuesta para que el middleware sepa que ya es la página común y no la vuelva a generar
    respuesta.pagina_error_comun = True

    # Devuelve la página de error
    return respuesta
