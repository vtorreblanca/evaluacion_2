# Migración inicial de la app 'tienda': crea las tablas de los 3 modelos relacionados
# (tienda_categoria, tienda_producto y tienda_valoracion), con la misma estructura que tenían en 'core'

# Importa los validadores de rango usados por la puntuación de Valoracion (1 a 5)
import django.core.validators
# Importa las reglas de borrado de las claves foráneas (PROTECT, CASCADE)
import django.db.models.deletion
# Importa las clases base de migración y los tipos de campo del ORM
from django.db import migrations, models


# Clase de la migración (Django la ejecuta con: python manage.py migrate)
class Migration(migrations.Migration):

    # Primera migración de la app: no depende de ninguna migración anterior de 'tienda'
    initial = True

    # No necesita que se haya ejecutado otra migración antes
    dependencies = [
    ]

    # Operaciones que se traducen a SQL (CREATE TABLE)
    operations = [
        # Crea la tabla de categorías (lado "1" de la relación Categoria 1 -> N Producto)
        migrations.CreateModel(
            name='Categoria',
            fields=[
                # Clave primaria autonumérica
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Nombre único de la categoría
                ('nombre', models.CharField(max_length=50, unique=True)),
                # Texto para la URL del filtro (?categoria=audio)
                ('slug', models.SlugField(help_text='Texto para la URL, sin espacios ni tildes (ej: audio, componentes)', max_length=60, unique=True)),
                # Descripción opcional
                ('descripcion', models.TextField(blank=True)),
            ],
            # Opciones del Meta del modelo
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['nombre'],
            },
        ),
        # Crea la tabla de productos, con su clave foránea hacia Categoria
        migrations.CreateModel(
            name='Producto',
            fields=[
                # Clave primaria autonumérica
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Código único del producto
                ('sku', models.CharField(help_text='Identificador único para el carrito (ej: b450, 99, 100)', max_length=50, unique=True)),
                # Nombre comercial
                ('nombre', models.CharField(max_length=150)),
                # Descripción del producto
                ('descripcion', models.TextField()),
                # Precio en pesos chilenos
                ('precio', models.IntegerField(help_text='Precio en pesos chilenos (sin puntos ni signos)')),
                # Ruta de la imagen dentro de media/productos/
                ('imagen', models.ImageField(upload_to='productos/')),
                # Disponible o no para la venta
                ('activo', models.BooleanField(default=True, help_text='Marcar si el producto está disponible para la venta')),
                # Fecha de creación automática
                ('creado', models.DateTimeField(auto_now_add=True)),
                # FK hacia Categoria: PROTECT impide borrar una categoría con productos; related_name='productos'
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='tienda.categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-creado'],
            },
        ),
        # Crea la tabla de valoraciones, con su clave foránea hacia Producto
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                # Clave primaria autonumérica
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Estrellas, validadas entre 1 y 5
                ('puntuacion', models.IntegerField(help_text='Calificación de 1 a 5 estrellas', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                # Texto de la opinión
                ('comentario', models.TextField()),
                # Fecha de creación automática
                ('creado', models.DateTimeField(auto_now_add=True)),
                # FK hacia Producto: CASCADE borra las valoraciones si se borra el producto; related_name='valoraciones'
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valoraciones', to='tienda.producto')),
            ],
            options={
                'verbose_name': 'Valoración',
                'verbose_name_plural': 'Valoraciones',
                'ordering': ['-creado'],
            },
        ),
    ]
