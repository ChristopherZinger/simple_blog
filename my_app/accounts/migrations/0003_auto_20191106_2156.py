# Generated by Django 2.2.2 on 2019-11-06 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_officeadmin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_active',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='admin',
        ),
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
