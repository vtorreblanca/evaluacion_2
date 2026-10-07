# Importa el módulo 'admin' provisto por Django para interactuar con la interfaz de administración
from django.contrib import admin

# Importa los modelos 'Producto' y 'Valoracion' definidos en el archivo models.py del mismo módulo/app
from .models import Producto, Valoracion


# Registra el modelo 'Producto' en el admin usando la clase de configuración 'ProductoAdmin'
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Define las columnas visibles en la vista de lista del panel para cada producto
    list_display = ('nombre', 'sku', 'categoria', 'precio', 'activo', 'creado')
    
    # Habilita un panel lateral derecho de filtros para segmentar por categoría y estado activo
    list_filter = ('categoria', 'activo')
    
    # Añade una barra de búsqueda para filtrar registros por coincidencia en nombre, SKU o descripción
    search_fields = ('nombre', 'sku', 'descripcion')
    
    # Permite editar directamente el precio y el estado activo desde la tabla sin entrar al detalle
    list_editable = ('precio', 'activo')


# Registra el modelo 'Valoracion' en el admin usando la clase de configuración 'ValoracionAdmin'
@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    # Define las columnas mostradas, incluyendo un método personalizado ('comentario_corto')
    list_display = ('producto', 'puntuacion', 'comentario_corto', 'creado')
    
    # Filtros laterales por puntaje y fecha de creación
    list_filter = ('puntuacion', 'creado')
    
    # Búsqueda por relación foránea (nombre del producto vinculado vía '__') y texto del comentario
    search_fields = ('producto__nombre', 'comentario')

    # Método para truncar comentarios extensos y evitar que deformen la tabla
    def comentario_corto(self, obj):
        # Toma los primeros 60 caracteres y añade '...' solo si la longitud original supera los 60
        return obj.comentario[:60] + ('...' if len(obj.comentario) > 60 else '')
    
    # Define el encabezado legible que tendrá esta columna calculada en la tabla del admin
    comentario_corto.short_description = "Comentario"
