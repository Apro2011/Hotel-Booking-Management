# Generated by Django 5.0.2 on 2024-02-19 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(choices=[('SB', 'Single Bed'), ('DB', 'Double Bed')], default='DB', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=250)),
                ('guest_phone', models.CharField(max_length=15)),
                ('guest_address', models.TextField(max_length=500)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('room_type', models.CharField(choices=[('SB', 'Single Bed'), ('DB', 'Double Bed')], default='DB', max_length=2)),
                ('room_assigned', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='booking.room')),
            ],
        ),
    ]
