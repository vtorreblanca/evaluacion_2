# Importa el módulo de administración nativo de Django para exponer el panel de control
from django.contrib import admin

# Importa la función path para definir patrones de ruta URL basados en cadenas sencillas y convertidores de tipo
from django.urls import path

# Importa el objeto global de configuración para acceder a las constantes definidas en settings.py (DEBUG, MEDIA_URL, etc.)
from django.conf import settings

# Importa el helper para servir archivos estáticos o multimedia a través del servidor de desarrollo de Django
from django.conf.urls.static import static

# Importa las funciones de vista definidas en el módulo views.py de la aplicación 'core'
from core import views


# Lista principal de rutas URL que Django evalúa secuencialmente de arriba hacia abajo
urlpatterns = [
    # Ruta hacia el panel administrativo (/admin/); delega la gestión a los endpoints internos del admin
    path('admin/', admin.site.urls),
    
    # Ruta raíz del sitio web (/); ejecuta la vista index encargada del catálogo de productos y filtros
    # name='index': identificador único para generar URLs dinámicas mediante {% url 'index' %} o reverse()
    path('', views.index, name='index'),
    
    # Endpoint POST para enviar reseñas; captura un número entero desde la URL (<int:producto_id>) y lo pasa como argumento a la vista
    # Ejemplo de URL resuelta: /producto/14/valorar/
    path('producto/<int:producto_id>/valorar/', views.agregar_valoracion, name='agregar_valoracion'),
    
    # Ruta para la página informativa "Quiénes Somos" (/about/)
    path('about/', views.about, name='about'),
    
    # Ruta para la página de vitrina o galería de productos (/gallery/)
    path('gallery/', views.gallery, name='gallery'),
    
    # Ruta para la sección de preguntas frecuentes (/faq/)
    path('faq/', views.faq, name='faq'),
]

# Condicional de entorno: solo si el proyecto corre en modo depuración (desarrollo local)
if settings.DEBUG:
    # Concatena a urlpatterns una regla para que el servidor local sirva las imágenes subidas por usuarios
    # settings.MEDIA_URL: el prefijo HTTP solicitado (ej: /media/)
    # document_root=settings.MEDIA_ROOT: la carpeta física en disco donde se buscan los archivos (ej: BASE_DIR / 'media')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
