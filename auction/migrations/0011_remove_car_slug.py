# Generated by Django 5.0.3 on 2024-03-16 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0010_car_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='slug',
        ),
    ]
