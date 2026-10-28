from django.contrib import admin

from .models import MensajeContacto


# Registra el modelo 'MensajeContacto' para revisar los mensajes del formulario de contacto
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'leido', 'creado')
    list_filter = ('asunto', 'leido', 'creado')
    search_fields = ('nombre', 'email', 'mensaje')
    list_editable = ('leido',)
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'creado')
