# Importa las clases base y los tipos de campo del ORM de Django
from django.db import models


# Define el modelo que almacena los mensajes enviados desde el formulario de contacto
class MensajeContacto(models.Model):
    # Opciones de motivo para clasificar las consultas recibidas
    ASUNTOS = [
        ('Consulta', 'Consulta general'),
        ('Producto', 'Información de un producto'),
        ('Pedido', 'Pedido o carrito'),
        ('Sugerencia', 'Sugerencia o reclamo'),
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

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-creado']

    def __str__(self):
        return f"{self.nombre} - {self.get_asunto_display()}"
