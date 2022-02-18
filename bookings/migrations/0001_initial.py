# Generated by Django 3.0.14 on 2022-02-18 05:25

import bookings.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.PositiveSmallIntegerField()),
                ('daily_rate', models.DecimalField(decimal_places=2, max_digits=20)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.RoomType')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('guest_count', models.PositiveSmallIntegerField()),
                ('contact_info', bookings.fields.ContactDetailsModelField()),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookings.Room')),
            ],
        ),
    ]