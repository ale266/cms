# Generated by Django 4.2.4 on 2023-10-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0002_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=500, verbose_name='Titulo'),
        ),
    ]