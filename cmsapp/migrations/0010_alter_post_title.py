# Generated by Django 4.2.4 on 2023-08-23 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0009_post_dislikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=500, verbose_name='Titulo'),
        ),
    ]
