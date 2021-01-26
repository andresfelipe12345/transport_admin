# Generated by Django 3.1.5 on 2021-01-15 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('routes', '0006_auto_20210115_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='place_destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='destination', to='places.place'),
        ),
        migrations.AlterField(
            model_name='route',
            name='place_origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='origin', to='places.place'),
        ),
    ]
