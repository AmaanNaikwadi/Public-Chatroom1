# Generated by Django 3.2 on 2021-07-21 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_rename_group_name_groupmember_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='last_message_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='last_active_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]