# Importa las clases base y los tipos de campo del ORM de Django
from django.db import models


# Define el modelo para registrar redes sociales manualmente desde el admin de Django
class RedSocial(models.Model):
    # Nombre del sitio o cuenta (ej: Inacap Shop)
    nombre_sitio = models.CharField(
        "Nombre del sitio",
        max_length=100,
        help_text="Ej: Inacap Shop",
    )

    # Nombre de la red social (ej: Instagram, Facebook, X, TikTok)
    red = models.CharField(
        "Red social",
        max_length=50,
        help_text="Ej: Instagram, Facebook, X, TikTok",
    )

    # Enlace completo al perfil (Django valida que sea una URL)
    link = models.URLField(
        "Link",
        help_text="Dirección completa, ej: https://www.instagram.com/inacapshop",
    )

    class Meta:
        verbose_name = "Red social"
        verbose_name_plural = "Redes sociales"
        ordering = ['nombre_sitio', 'red']

    def __str__(self):
        return f"{self.nombre_sitio} - {self.red}"
