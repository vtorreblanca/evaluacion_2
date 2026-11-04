# Importa el módulo 'admin' provisto por Django para interactuar con la interfaz de administración
from django.contrib import admin

# Importa los modelos 'Categoria', 'Producto' y 'Valoracion' definidos en el archivo models.py del mismo módulo/app
from .models import Categoria, Producto, Valoracion


# Registra el modelo 'Categoria' en el admin usando la clase de configuración 'CategoriaAdmin'
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Columnas visibles: nombre, slug y una columna calculada con la cantidad de productos
    list_display = ('nombre', 'slug', 'cantidad_productos')

    # Búsqueda por nombre o descripción
    search_fields = ('nombre', 'descripcion')

    # Rellena automáticamente el slug mientras se escribe el nombre en el formulario
    prepopulated_fields = {'slug': ('nombre',)}

    # Cuenta los productos asociados usando la relación inversa related_name='productos'
    def cantidad_productos(self, obj):
        # obj es la categoría de la fila; obj.productos.count() devuelve cuántos productos tiene asociados
        return obj.productos.count()

    # Define el encabezado legible que tendrá esta columna calculada en la tabla del admin
    cantidad_productos.short_description = "Productos"


# Inline: permite ver y agregar valoraciones dentro de la página de edición de cada producto
# TabularInline las muestra como una tabla (una fila por valoración)
class ValoracionInline(admin.TabularInline):
    # Modelo que se muestra dentro del producto (relacionado por la FK Valoracion.producto)
    model = Valoracion
    # Cantidad de filas vacías extra para agregar nuevas valoraciones
    extra = 1
    # Campos que se muestran en cada fila
    fields = ('puntuacion', 'comentario', 'creado')
    # 'creado' se llena automáticamente (auto_now_add), por eso solo se puede leer
    readonly_fields = ('creado',)


# Registra el modelo 'Producto' en el admin usando la clase de configuración 'ProductoAdmin'
# (este admin tiene 11 atributos de personalización: requisito de al menos 7 en un admin.py)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # 1. Define las columnas visibles en la vista de lista del panel para cada producto
    list_display = ('nombre', 'sku', 'categoria', 'precio', 'activo', 'creado')
    
    # 2. Habilita un panel lateral derecho de filtros para segmentar por categoría y estado activo
    list_filter = ('categoria', 'activo')
    
    # 3. Añade una barra de búsqueda para filtrar registros por coincidencia en nombre, SKU o descripción
    search_fields = ('nombre', 'sku', 'descripcion')
    
    # 4. Permite editar directamente el precio y el estado activo desde la tabla sin entrar al detalle
    list_editable = ('precio', 'activo')

    # 5. Columna que funciona como enlace para abrir el detalle del producto
    list_display_links = ('nombre',)

    # 6. Cantidad de productos que se muestran por página en la lista del admin
    list_per_page = 10

    # 7. Orden por defecto de la lista: primero por categoría y luego por nombre (A-Z)
    ordering = ('categoria__nombre', 'nombre')

    # 8. Barra de navegación por fechas (año / mes / día) sobre el campo 'creado'
    date_hierarchy = 'creado'

    # 9. Campos que se ven en el formulario pero no se pueden modificar
    readonly_fields = ('creado',)

    # 10. Agrupa los campos del formulario de edición en secciones con título
    fieldsets = (
        # Sección 1: datos que identifican al producto
        ('Datos del producto', {
            'fields': ('sku', 'nombre', 'categoria', 'descripcion'),
        }),
        # Sección 2: precio y disponibilidad para la venta
        ('Venta', {
            'fields': ('precio', 'activo'),
        }),
        # Sección 3: imagen del producto
        ('Imagen', {
            'fields': ('imagen',),
        }),
        # Sección 4: información automática; 'collapse' la muestra plegada
        ('Información del sistema', {
            'fields': ('creado',),
            'classes': ('collapse',),
        }),
    )

    # 11. Muestra las valoraciones del producto dentro de su página de edición (definido arriba)
    inlines = [ValoracionInline]


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
