# Generated by Django 2.2.2 on 2019-11-17 11:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20191117_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 17, 12, 2, 37, 807174)),
        ),
    ]
