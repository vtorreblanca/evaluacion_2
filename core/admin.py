from django.contrib import admin
from .models import Producto, Valoracion

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'categoria', 'precio', 'activo', 'creado')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'sku', 'descripcion')
    list_editable = ('precio', 'activo')

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'puntuacion', 'comentario_corto', 'creado')
    list_filter = ('puntuacion', 'creado')
    search_fields = ('producto__nombre', 'comentario')

    def comentario_corto(self, obj):
        return obj.comentario[:60] + ('...' if len(obj.comentario) > 60 else '')
    comentario_corto.short_description = "Comentario"
