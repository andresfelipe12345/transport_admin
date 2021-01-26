# Generated by Django 3.1.5 on 2021-01-15 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('routes', '0002_auto_20210115_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='place_destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='destination', to='places.place'),
        ),
        migrations.AlterField(
            model_name='route',
            name='place_origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='origin', to='places.place'),
        ),
    ]