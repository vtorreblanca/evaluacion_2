# Importa las clases base y los tipos de campo del ORM de Django
from django.db import models


# Define el modelo para registrar redes sociales manualmente desde el admin de Django
class RedSocial(models.Model):
    # Nombre del sitio o cuenta (ej: Inacap Shop)
    nombre_sitio = models.CharField(
        "Nombre del sitio",                 # Nombre legible del campo (se ve como etiqueta en el admin)
        max_length=100,                     # Largo máximo del texto
        help_text="Ej: Inacap Shop",        # Texto de ayuda bajo el campo en el admin
    )

    # Nombre de la red social (ej: Instagram, Facebook, X, TikTok)
    red = models.CharField(
        "Red social",                                   # Etiqueta del campo en el admin
        max_length=50,                                  # Largo máximo del texto
        help_text="Ej: Instagram, Facebook, X, TikTok", # Texto de ayuda en el admin
    )

    # Enlace completo al perfil (Django valida que sea una URL)
    link = models.URLField(
        "Link",                                                                  # Etiqueta del campo en el admin
        help_text="Dirección completa, ej: https://www.instagram.com/inacapshop", # Texto de ayuda en el admin
    )

    # Metadatos del modelo
    class Meta:
        verbose_name = "Red social"             # Nombre singular en el admin
        verbose_name_plural = "Redes sociales"  # Nombre plural en el admin
        ordering = ['nombre_sitio', 'red']      # Orden por defecto: por sitio y luego por red (A-Z)

    # Representación en texto del objeto (se ve en el admin)
    def __str__(self):
        # Devuelve, por ejemplo, "Inacap Shop - Instagram"
        return f"{self.nombre_sitio} - {self.red}"
