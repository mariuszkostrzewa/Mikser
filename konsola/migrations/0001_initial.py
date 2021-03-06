# Generated by Django 2.0 on 2017-12-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pomiar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ec', models.DecimalField(decimal_places=3, max_digits=4)),
                ('ph', models.DecimalField(decimal_places=3, max_digits=4)),
                ('temp', models.DecimalField(decimal_places=3, max_digits=4)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
