from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'categoria', 'precio', 'activo', 'creado')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'sku', 'descripcion')
    list_editable = ('precio', 'activo')
