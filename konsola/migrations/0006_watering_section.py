# Generated by Django 2.0 on 2017-12-30 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('konsola', '0005_auto_20171230_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='watering',
            name='section',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='konsola.Section'),
            preserve_default=False,
        ),
    ]
