# Generated by Django 3.2 on 2021-07-21 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_notification_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupthread',
            name='name',
        ),
        migrations.AddField(
            model_name='groupthread',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='chat.group'),
            preserve_default=False,
        ),
    ]