# Generated by Django 4.2.4 on 2023-10-19 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0006_delete_rolusuario'),
        ('cmsapp', '0015_post_miembros_post_roles_rolusuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='miembros',
            field=models.ManyToManyField(related_name='set_miembros', to=settings.AUTH_USER_MODEL, verbose_name='Miembros'),
        ),
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.userprofile', verbose_name='Creador'),
        ),
    ]