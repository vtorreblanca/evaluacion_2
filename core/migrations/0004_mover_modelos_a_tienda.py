# Elimina de la app 'core' los modelos Categoria, Producto y Valoracion, que ahora viven en la app 'tienda'.
# Se ejecuta DESPUÉS de que tienda/migrations/0002 copió todos los datos a las tablas nuevas.

# Importa las clases base de migración
from django.db import migrations


class Migration(migrations.Migration):

    # Depende de la última migración de 'core' y de la copia de datos hecha en 'tienda'
    dependencies = [
        ('core', '0003_categoria'),
        ('tienda', '0002_copiar_datos_desde_core'),
    ]

    # Borra las tablas antiguas en orden: primero la que tiene la FK (Valoracion -> Producto -> Categoria)
    operations = [
        migrations.DeleteModel(name='Valoracion'),
        migrations.DeleteModel(name='Producto'),
        migrations.DeleteModel(name='Categoria'),
    ]
