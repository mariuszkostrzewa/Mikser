# Generated by Django 2.0 on 2018-07-10 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('konsola', '0006_watering_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='read',
            name='ec',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='read',
            name='ph',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]