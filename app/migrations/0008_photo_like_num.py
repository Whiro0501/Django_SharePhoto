# Generated by Django 2.2.3 on 2019-07-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190727_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='like_num',
            field=models.IntegerField(default=0),
        ),
    ]
