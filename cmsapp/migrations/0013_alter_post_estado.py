# Generated by Django 4.2.4 on 2023-12-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0012_remove_post_carrousel_remove_post_tipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='estado',
            field=models.CharField(choices=[('En Creacion', 'En Creacion'), ('En Edicion', 'En Edicion'), ('En Publicacion', 'En Publicacion'), ('Desactivado', 'Desactivado')], default='En Creacion', max_length=20),
        ),
    ]