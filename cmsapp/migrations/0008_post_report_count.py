# Generated by Django 4.2.4 on 2023-11-02 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0007_report_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='report_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
