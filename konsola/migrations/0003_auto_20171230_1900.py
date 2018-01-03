# Generated by Django 2.0 on 2017-12-30 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('konsola', '0002_auto_20171227_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proportion', models.IntegerField()),
                ('ec', models.DecimalField(decimal_places=3, max_digits=4)),
                ('ph', models.DecimalField(decimal_places=3, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valve', models.IntegerField()),
                ('description', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='konsola.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='acid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acidBarrel', to='konsola.Section'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fertilizerI',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fert1', to='konsola.Section'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fertilizerII',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fert2', to='konsola.Section'),
        ),
    ]