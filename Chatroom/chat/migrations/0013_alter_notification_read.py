# Generated by Django 3.2 on 2021-07-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.IntegerField(default=0),
        ),
    ]
