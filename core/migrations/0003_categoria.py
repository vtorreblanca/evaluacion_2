# Migración escrita a mano para convertir la categoría de Producto (texto fijo) en un modelo Categoria.
# Se hace en varios pasos para NO perder la categoría de los productos que ya existen en la BD.

# Importa las reglas de borrado (PROTECT, CASCADE, etc.) usadas por las claves foráneas
import django.db.models.deletion
# Importa las clases base de migración y los tipos de campo del ORM
from django.db import migrations, models
# slugify convierte un texto en formato URL (ej: "Audio" -> "audio")
from django.utils.text import slugify


# Descripciones iniciales para las categorías que ya usaba la tienda
DESCRIPCIONES = {
    'Componentes': 'Piezas internas para armar o mejorar tu PC.',
    'Audio': 'Audífonos, parlantes y micrófonos.',
    'Accesorios': 'Periféricos y complementos para tu equipo.',
}


def pasar_texto_a_categoria(apps, schema_editor):
    """Crea una Categoria por cada texto distinto y la asigna a cada producto."""
    # Obtiene el modelo Producto tal como estaba en este punto de las migraciones (versión histórica)
    Producto = apps.get_model('core', 'Producto')
    # Obtiene el modelo Categoria recién creado en el paso 1 de esta migración
    Categoria = apps.get_model('core', 'Categoria')

    # Asegura que existan las 3 categorías originales aunque no tengan productos
    # Recorre el diccionario DESCRIPCIONES obteniendo cada nombre con su descripción
    for nombre, descripcion in DESCRIPCIONES.items():
        # get_or_create busca la categoría por nombre y, si no existe, la crea
        Categoria.objects.get_or_create(
            # Campo por el que se busca
            nombre=nombre,
            # Valores que solo se usan si hay que crearla (slug generado desde el nombre y su descripción)
            defaults={'slug': slugify(nombre), 'descripcion': descripcion},
        )

    # Copia el texto antiguo (campo 'categoria') a la nueva clave foránea ('categoria_nueva')
    # Recorre todos los productos existentes en la BD
    for producto in Producto.objects.all():
        # Lee el texto antiguo de la categoría; si estuviera vacío usa 'Componentes' (el default anterior)
        nombre = producto.categoria or 'Componentes'
        # Busca (o crea si fuera una categoría distinta) la Categoria con ese nombre; '_' descarta el booleano "creado"
        categoria, _ = Categoria.objects.get_or_create(
            # Campo por el que se busca
            nombre=nombre,
            # Slug que se usa solo si hay que crearla
            defaults={'slug': slugify(nombre)},
        )
        # Asigna la categoría encontrada a la nueva clave foránea del producto
        producto.categoria_nueva = categoria
        # Guarda solo ese campo en la BD (update_fields evita reescribir el resto de columnas)
        producto.save(update_fields=['categoria_nueva'])


def pasar_categoria_a_texto(apps, schema_editor):
    """Operación inversa (si se deshace la migración): vuelve a guardar el nombre como texto."""
    # Obtiene la versión histórica del modelo Producto
    Producto = apps.get_model('core', 'Producto')
    # Recorre todos los productos
    for producto in Producto.objects.all():
        # Copia el nombre de la categoría (FK) al campo de texto antiguo; si no tiene, usa 'Componentes'
        producto.categoria = producto.categoria_nueva.nombre if producto.categoria_nueva else 'Componentes'
        # Guarda solo el campo de texto
        producto.save(update_fields=['categoria'])


# Define la clase de migración que Django ejecuta con "python manage.py migrate"
class Migration(migrations.Migration):

    # Esta migración solo se ejecuta después de la migración 0002 (la que creó Valoracion)
    dependencies = [
        ('core', '0002_valoracion'),
    ]

    # Lista de operaciones que se aplican en orden sobre la BD
    operations = [
        # 1. Crea la tabla core_categoria
        migrations.CreateModel(
            # Nombre del modelo (la tabla se llamará core_categoria)
            name='Categoria',
            fields=[
                # Clave primaria autonumérica de 64 bits
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Nombre único de la categoría
                ('nombre', models.CharField(max_length=50, unique=True)),
                # Slug único para usar en la URL del filtro
                ('slug', models.SlugField(help_text='Texto para la URL, sin espacios ni tildes (ej: audio, componentes)', max_length=60, unique=True)),
                # Descripción opcional (blank=True permite dejarla vacía)
                ('descripcion', models.TextField(blank=True)),
            ],
            # Opciones de la clase Meta del modelo
            options={
                'verbose_name': 'Categoría',            # Nombre singular en el admin
                'verbose_name_plural': 'Categorías',    # Nombre plural en el admin
                'ordering': ['nombre'],                 # Orden alfabético por defecto
            },
        ),

        # 2. Agrega una FK temporal (permite nulos mientras se copian los datos)
        migrations.AddField(
            model_name='producto',          # Modelo al que se agrega el campo
            name='categoria_nueva',         # Nombre temporal del campo
            # null=True permite que quede vacío mientras se copian los datos; related_name='+' no crea relación inversa
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.categoria'),
        ),

        # 3. Copia los datos del texto antiguo a la FK
        # (primera función = al migrar; segunda función = al deshacer la migración)
        migrations.RunPython(pasar_texto_a_categoria, pasar_categoria_a_texto),

        # 4. Elimina el campo de texto antiguo
        migrations.RemoveField(
            model_name='producto',          # Modelo del que se elimina el campo
            name='categoria',               # Campo de texto antiguo (CharField con choices)
        ),

        # 5. Renombra la FK temporal a 'categoria'
        migrations.RenameField(
            model_name='producto',          # Modelo en el que se renombra el campo
            old_name='categoria_nueva',     # Nombre temporal
            new_name='categoria',           # Nombre definitivo (columna categoria_id en la BD)
        ),

        # 6. Deja la FK definitiva: obligatoria y con related_name='productos'
        migrations.AlterField(
            model_name='producto',          # Modelo que se modifica
            name='categoria',               # Campo que se modifica
            # Sin null=True (ahora es obligatorio); PROTECT impide borrar categorías con productos; related_name='productos'
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='core.categoria'),
        ),
    ]
