# Generated by Django 3.1.5 on 2021-01-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buses', '0003_remove_bus_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bus', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='buses.bus')),
            ],
        ),
    ]
