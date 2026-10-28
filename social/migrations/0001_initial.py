from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sitio', models.CharField(help_text='Ej: Inacap Shop', max_length=100, verbose_name='Nombre del sitio')),
                ('red', models.CharField(help_text='Ej: Instagram, Facebook, X, TikTok', max_length=50, verbose_name='Red social')),
                ('link', models.URLField(help_text='Dirección completa, ej: https://www.instagram.com/inacapshop', verbose_name='Link')),
            ],
            options={
                'verbose_name': 'Red social',
                'verbose_name_plural': 'Redes sociales',
                'ordering': ['nombre_sitio', 'red'],
            },
        ),
    ]
