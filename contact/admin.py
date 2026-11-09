# Importa el módulo de administración de Django
from django.contrib import admin

# Importa el modelo de esta app que se va a mostrar en el admin
from .models import MensajeContacto


# Registra el modelo 'MensajeContacto' para revisar los mensajes del formulario de contacto
@admin.register(MensajeContacto)
# Clase de configuración del admin para los mensajes (hereda de ModelAdmin)
class MensajeContactoAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista de mensajes
    list_display = ('nombre', 'email', 'asunto', 'leido', 'creado')
    # Filtros del panel lateral derecho: por motivo, por leído/no leído y por fecha
    list_filter = ('asunto', 'leido', 'creado')
    # Barra de búsqueda: busca coincidencias en nombre, email o texto del mensaje
    search_fields = ('nombre', 'email', 'mensaje')
    # Permite marcar 'leido' directamente desde la lista, sin entrar al detalle
    list_editable = ('leido',)
    # Campos que se ven pero no se pueden modificar (el mensaje lo escribió el cliente, no se debe alterar)
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'creado')
