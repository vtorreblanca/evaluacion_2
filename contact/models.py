# Importa las clases base y los tipos de campo del ORM de Django
from django.db import models


# Define el modelo que almacena los mensajes enviados desde el formulario de contacto
class MensajeContacto(models.Model):
    # Opciones de motivo para clasificar las consultas recibidas
    # Cada opción es una tupla (valor que se guarda en la BD, texto que ve el usuario)
    ASUNTOS = [
        ('Consulta', 'Consulta general'),            # Se guarda 'Consulta' y se muestra 'Consulta general'
        ('Producto', 'Información de un producto'),  # Se guarda 'Producto' y se muestra 'Información de un producto'
        ('Pedido', 'Pedido o carrito'),              # Se guarda 'Pedido' y se muestra 'Pedido o carrito'
        ('Sugerencia', 'Sugerencia o reclamo'),      # Se guarda 'Sugerencia' y se muestra 'Sugerencia o reclamo'
    ]

    # Nombre de la persona que escribe
    nombre = models.CharField(max_length=100)

    # Correo electrónico de respuesta (validado como email por Django)
    email = models.EmailField()

    # Motivo del mensaje basado en la lista ASUNTOS
    asunto = models.CharField(max_length=20, choices=ASUNTOS, default='Consulta')

    # Cuerpo del mensaje
    mensaje = models.TextField()

    # Permite marcar desde el admin si el mensaje ya fue revisado
    leido = models.BooleanField(default=False)

    # Fecha y hora de envío
    creado = models.DateTimeField(auto_now_add=True)

    # Metadatos del modelo (configuración que no es un campo de la tabla)
    class Meta:
        verbose_name = "Mensaje de contacto"           # Nombre singular en el admin
        verbose_name_plural = "Mensajes de contacto"   # Nombre plural en el admin
        ordering = ['-creado']                         # Orden por defecto: mensajes más recientes primero

    # Representación en texto del objeto (se ve en el admin y en la consola)
    def __str__(self):
        # get_asunto_display() devuelve el texto legible de la opción elegida (ej: 'Consulta general')
        return f"{self.nombre} - {self.get_asunto_display()}"
