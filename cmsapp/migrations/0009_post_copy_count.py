# Generated by Django 4.2.4 on 2023-11-14 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0008_post_report_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='copy_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
