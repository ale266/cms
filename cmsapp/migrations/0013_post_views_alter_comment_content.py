# Generated by Django 4.2.4 on 2023-09-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0012_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(help_text='Escriba un comentario...', max_length=2000, verbose_name='Comentario'),
        ),
    ]
