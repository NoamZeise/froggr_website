# Generated by Django 4.1 on 2023-03-06 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('froggr', '0009_blogpost_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.datetime(1900, 1, 1, 0, 0)),
        ),
    ]
