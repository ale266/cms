# Generated by Django 4.2.4 on 2023-11-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0008_post_report_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='historia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_slug', models.SlugField(null=True)),
                ('evento', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='historial',
            field=models.ManyToManyField(to='cmsapp.historia'),
        ),
    ]