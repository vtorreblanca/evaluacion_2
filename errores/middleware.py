# Importa la configuración del proyecto (para leer STATIC_URL y MEDIA_URL)
from django.conf import settings

# Importa la excepción Http404 que lanzan las vistas cuando no encuentran algo
from django.http import Http404

# Importa la vista común de error de esta misma app
from .views import pagina_404


# Prefijos de URL que NO deben usar la página común (el admin tiene la suya; estáticos y media son archivos)
RUTAS_EXCLUIDAS = ('/admin/', settings.STATIC_URL, settings.MEDIA_URL)


class Error404Middleware:
    """
    Middleware que envía todos los errores 404 del sitio a la página común de errores.
    Es necesario porque con DEBUG = True Django ignora handler404 y muestra su página amarilla de depuración.
    """

    def __init__(self, get_response):
        # Django entrega la función que procesa la petición (siguiente middleware o la vista); se guarda para usarla después
        self.get_response = get_response

    def __call__(self, request):
        # Deja que la petición siga su camino normal y obtiene la respuesta
        response = self.get_response(request)

        # Reemplaza la respuesta por la página común solo si:
        if (
            response.status_code == 404                                      # es un error 404,
            and not getattr(response, 'pagina_error_comun', False)           # todavía no es la página común,
            and not self._ruta_excluida(request)                             # no es admin, estáticos ni media,
            and 'application/json' not in response.get('Content-Type', '')   # y no es una respuesta JSON (fetch del carrito/valoraciones)
        ):
            # Devuelve la página común (cubre, por ejemplo, URLs que no existen)
            return pagina_404(request)

        # En cualquier otro caso devuelve la respuesta original sin cambios
        return response

    def process_exception(self, request, exception):
        # Django llama a este método cuando una vista lanza una excepción (ej: raise Http404 o get_object_or_404)
        if isinstance(exception, Http404) and not self._ruta_excluida(request):
            # Devuelve la página común, pasando la excepción para mostrar su mensaje
            return pagina_404(request, exception)
        # None: Django sigue con su manejo normal para cualquier otra excepción
        return None

    def _ruta_excluida(self, request):
        # True si la ruta pedida comienza con alguno de los prefijos excluidos
        return request.path.startswith(RUTAS_EXCLUIDAS)
