# Generated by Django 4.2.4 on 2023-08-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_alter_userprofile_about'),
        ('cmsapp', '0008_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(related_name='blog_post2', to='userprofile.userprofile'),
        ),
    ]
