# Generated by Django 3.2 on 2021-07-24 17:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_threadmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadmessage',
            name='time',
            field=models.TimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
