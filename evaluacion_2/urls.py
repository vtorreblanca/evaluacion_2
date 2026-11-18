# Importa el módulo de administración nativo de Django para exponer el panel de control
from django.contrib import admin

# Importa la función path para definir patrones de ruta URL basados en cadenas sencillas y convertidores de tipo
from django.urls import path, include

# Importa el objeto global de configuración para acceder a las constantes definidas en settings.py (DEBUG, MEDIA_URL, etc.)
from django.conf import settings

# Importa el helper para servir archivos estáticos o multimedia a través del servidor de desarrollo de Django
from django.conf.urls.static import static

# Lista principal de rutas URL que Django evalúa secuencialmente de arriba hacia abajo
urlpatterns = [
    # Ruta hacia el panel administrativo (/admin/); delega la gestión a los endpoints internos del admin
    path('admin/', admin.site.urls),
    
    # Rutas de la app 'tienda' (/, /producto/<id>/valorar/, /gallery/); están en tienda/urls.py
    path('', include('tienda.urls')),

    # Rutas de la app 'core' (/about/, /faq/); están en core/urls.py
    path('', include('core.urls')),

    # Ruta hacia la app 'contact' (/contacto/); sus rutas internas están en contact/urls.py
    path('contacto/', include('contact.urls')),
]

# Vista común (app 'errores') que Django usa para el error 404 en todo el sitio cuando DEBUG = False
# (con DEBUG = True lo hace el middleware errores.middleware.Error404Middleware)
# Variable especial de Django: indica (como texto 'app.modulo.funcion') qué vista responde los errores 404
handler404 = 'errores.views.pagina_404'

# Condicional de entorno: solo si el proyecto corre en modo depuración (desarrollo local)
if settings.DEBUG:
    # Concatena a urlpatterns una regla para que el servidor local sirva las imágenes subidas por usuarios
    # settings.MEDIA_URL: el prefijo HTTP solicitado (ej: /media/)
    # document_root=settings.MEDIA_ROOT: la carpeta física en disco donde se buscan los archivos (ej: BASE_DIR / 'media')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
