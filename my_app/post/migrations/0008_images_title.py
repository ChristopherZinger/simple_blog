# Generated by Django 2.2.2 on 2019-12-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20191201_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
