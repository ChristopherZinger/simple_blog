# Generated by Django 2.2.2 on 2019-11-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='officeadmin',
            field=models.BooleanField(default=False),
        ),
    ]
