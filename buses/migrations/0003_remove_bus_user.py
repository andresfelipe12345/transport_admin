# Generated by Django 3.1.5 on 2021-01-17 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0002_bus_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='user',
        ),
    ]