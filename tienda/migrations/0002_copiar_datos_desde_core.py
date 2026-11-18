# Migración de datos: copia las categorías, productos y valoraciones que estaban en la app 'core'
# a las tablas nuevas de la app 'tienda', manteniendo los mismos id y fechas (no se pierde nada).
# En una base de datos nueva (vacía) simplemente no copia nada.

# Importa las clases base de migración
from django.db import migrations


def copiar_desde_core(apps, schema_editor):
    """Copia cada registro de core_* a tienda_* conservando su id y su fecha de creación."""
    # Modelos de origen (versión histórica, tal como estaban en 'core')
    CategoriaCore = apps.get_model('core', 'Categoria')
    ProductoCore = apps.get_model('core', 'Producto')
    ValoracionCore = apps.get_model('core', 'Valoracion')
    # Modelos de destino (las tablas nuevas de 'tienda')
    Categoria = apps.get_model('tienda', 'Categoria')
    Producto = apps.get_model('tienda', 'Producto')
    Valoracion = apps.get_model('tienda', 'Valoracion')

    # 1. Categorías (se copian primero porque los productos apuntan a ellas)
    for c in CategoriaCore.objects.all():
        # Se crea con el mismo id para que las claves foráneas sigan calzando
        Categoria.objects.create(id=c.id, nombre=c.nombre, slug=c.slug, descripcion=c.descripcion)

    # 2. Productos (apuntan a la categoría por su id: categoria_id)
    for p in ProductoCore.objects.all():
        Producto.objects.create(
            id=p.id, sku=p.sku, nombre=p.nombre, categoria_id=p.categoria_id,
            descripcion=p.descripcion, precio=p.precio, imagen=p.imagen.name, activo=p.activo,
        )
        # 'creado' tiene auto_now_add (al crear se pondría la fecha de hoy), por eso
        # se restaura la fecha original con update(), que escribe directo en la BD
        Producto.objects.filter(id=p.id).update(creado=p.creado)

    # 3. Valoraciones (apuntan al producto por su id: producto_id)
    for v in ValoracionCore.objects.all():
        Valoracion.objects.create(id=v.id, producto_id=v.producto_id, puntuacion=v.puntuacion, comentario=v.comentario)
        # Restaura la fecha original de la valoración
        Valoracion.objects.filter(id=v.id).update(creado=v.creado)


class Migration(migrations.Migration):

    # Necesita las tablas nuevas de 'tienda' (0001) y la última versión de los modelos en 'core' (0003)
    dependencies = [
        ('tienda', '0001_initial'),
        ('core', '0003_categoria'),
    ]

    # RunPython ejecuta la función de copia; al deshacer la migración no hace nada (noop)
    operations = [
        migrations.RunPython(copiar_desde_core, migrations.RunPython.noop),
    ]
