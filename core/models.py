from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('Componentes', 'Componentes'),
        ('Audio', 'Audio'),
        ('Accesorios', 'Accesorios'),
    ]

    sku = models.CharField(max_length=50, unique=True, help_text="Identificador único para el carrito (ej: b450, 99, 100)")
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='Componentes')
    descripcion = models.TextField()
    precio = models.IntegerField(help_text="Precio en pesos chilenos (sin puntos ni signos)")
    imagen = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True, help_text="Marcar si el producto está disponible para la venta")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-creado']

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
