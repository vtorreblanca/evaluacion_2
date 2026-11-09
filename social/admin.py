# Importa el módulo de administración de Django
from django.contrib import admin

# Importa el modelo de esta app que se va a mostrar en el admin
from .models import RedSocial


# Registra el modelo 'RedSocial' para agregar y editar redes sociales de forma manual
@admin.register(RedSocial)
# Clase de configuración del admin para las redes sociales (hereda de ModelAdmin)
class RedSocialAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista del panel
    list_display = ('nombre_sitio', 'red', 'link')
    # Filtro lateral por red social
    list_filter = ('red',)
    # Barra de búsqueda por nombre del sitio, red o link
    search_fields = ('nombre_sitio', 'red', 'link')
    # Orden de los campos en el formulario de creación/edición
    fields = ('nombre_sitio', 'red', 'link')
