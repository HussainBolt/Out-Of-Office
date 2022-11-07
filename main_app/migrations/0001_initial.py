# Generated by Django 4.1.1 on 2022-11-01 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_name', models.CharField(max_length=100)),
                ('locations', models.TextField(max_length=250)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField(max_length=250)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.trip')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=100)),
                ('time', models.DateTimeField(verbose_name='Time Slot')),
                ('locations', models.TextField(max_length=250)),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.itinerary')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
