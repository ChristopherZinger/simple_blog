# Generated by Django 2.2.2 on 2019-11-22 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20191122_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 22, 10, 43, 44, 309898)),
        ),
    ]
