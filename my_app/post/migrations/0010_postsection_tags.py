# Generated by Django 2.2.2 on 2019-12-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20191216_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsection',
            name='tags',
            field=models.CharField(default='<p>,</p>', max_length=255),
        ),
    ]
