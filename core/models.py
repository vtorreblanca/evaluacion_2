# Importa las clases base y los tipos de campo del ORM de Django
from django.db import models

# Importa validadores numéricos estándar para restringir rangos de valores a nivel de modelo/formulario
from django.core.validators import MinValueValidator, MaxValueValidator


# Define el modelo de categorías de la tienda (tabla propia en la BD)
# Antes la categoría era un texto fijo dentro de Producto; ahora es un modelo independiente
# para poder administrarla desde el admin y relacionarla con los productos (relación 1 a N)
class Categoria(models.Model):
    # Nombre visible de la categoría (ej: Audio); único para no repetir categorías
    nombre = models.CharField(max_length=50, unique=True)

    # Versión "amigable para URL" del nombre (ej: audio); se usará para filtrar por GET (?categoria=audio)
    slug = models.SlugField(
        max_length=60,                             # Largo máximo del texto
        unique=True,                               # No pueden existir dos categorías con el mismo slug
        help_text="Texto para la URL, sin espacios ni tildes (ej: audio, componentes)"  # Ayuda que se ve en el admin
    )

    # Descripción opcional de la categoría
    descripcion = models.TextField(blank=True)

    # Metadatos del modelo Categoria
    class Meta:
        verbose_name = "Categoría"                 # Nombre singular en la interfaz de administración
        verbose_name_plural = "Categorías"         # Nombre plural en la interfaz de administración
        ordering = ['nombre']                      # Orden alfabético por defecto

    # Representación en texto: muestra solo el nombre (así {{ producto.categoria }} sigue mostrando "Audio")
    def __str__(self):
        # Devuelve el nombre de la categoría como texto
        return self.nombre


# Define el modelo de datos para los productos de la tienda (tabla en la BD)
class Producto(models.Model):
    # Código único de producto (SKU), limitado a 50 caracteres y con índice único en BD
    sku = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Identificador único para el carrito (ej: b450, 99, 100)"
    )
    
    # Nombre comercial del producto con un límite de 150 caracteres
    nombre = models.CharField(max_length=150)
    
    # Clave foránea hacia Categoria: relación 1 a N (una categoría tiene muchos productos)
    # on_delete=models.PROTECT: impide borrar una categoría que todavía tiene productos asociados
    # related_name='productos': permite acceder desde la categoría con `categoria.productos.all()`
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    
    # Descripción detallada del producto (se traduce en un tipo TEXT sin límite estricto en BD)
    descripcion = models.TextField()
    
    # Precio unitario entero (adecuado para monedas sin decimales como el peso chileno CLP)
    precio = models.IntegerField(help_text="Precio en pesos chilenos (sin puntos ni signos)")
    
    # Archivo de imagen subido al subdirectorio 'MEDIA_ROOT/productos/'
    imagen = models.ImageField(upload_to='productos/')
    
    # Flag booleano para habilitar/deshabilitar la visibilidad o venta sin borrar el registro
    activo = models.BooleanField(
        default=True, 
        help_text="Marcar si el producto está disponible para la venta"
    )
    
    # Marca temporal automática al momento de crearse el registro (no editable)
    creado = models.DateTimeField(auto_now_add=True)

    # Metadatos de configuración del modelo
    class Meta:
        verbose_name = "Producto"                  # Nombre singular en la interfaz de administración
        verbose_name_plural = "Productos"          # Nombre plural en la interfaz de administración
        ordering = ['-creado']                     # Orden predeterminado: más recientes primero (orden descendente)

    # Representación en cadena de texto del objeto (usado en admin, logs y templates)
    def __str__(self):
        return f"{self.nombre} (${self.precio})"


# Define el modelo de calificaciones y opiniones asociadas a un producto
class Valoracion(models.Model):
    # Clave foránea hacia Producto: relación 1 a N (un producto tiene muchas valoraciones)
    # on_delete=models.CASCADE: si se borra el producto, se eliminan todas sus valoraciones
    # related_name='valoraciones': permite acceder desde el producto con `producto.valoraciones.all()`
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='valoraciones')
    
    # Puntaje numérico entero validado en un rango cerrado de 1 a 5
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    
    # Texto libre de la opinión dejada por el usuario
    comentario = models.TextField()
    
    # Fecha y hora exacta de registro de la valoración
    creado = models.DateTimeField(auto_now_add=True)

    # Metadatos del modelo Valoracion
    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        ordering = ['-creado']                     # Orden descendente por fecha de publicación

    # Representación legible mostrando el nombre del producto vinculado y las estrellas
    def __str__(self):
        return f"{self.producto.nombre} - {self.puntuacion}★"
