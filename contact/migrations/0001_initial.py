from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MensajeContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('asunto', models.CharField(choices=[('Consulta', 'Consulta general'), ('Producto', 'Información de un producto'), ('Pedido', 'Pedido o carrito'), ('Sugerencia', 'Sugerencia o reclamo')], default='Consulta', max_length=20)),
                ('mensaje', models.TextField()),
                ('leido', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Mensaje de contacto',
                'verbose_name_plural': 'Mensajes de contacto',
                'ordering': ['-creado'],
            },
        ),
    ]
