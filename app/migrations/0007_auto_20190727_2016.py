# Generated by Django 2.2.3 on 2019-07-27 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post',
            new_name='photos',
        ),
    ]
