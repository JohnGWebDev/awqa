# Generated by Django 5.1.1 on 2024-11-09 02:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aquarium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('is_private', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FreshWaterParameterLogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('ph', models.CharField(choices=[('6.0', '6.0'), ('6.4', '6.4'), ('6.6', '6.6'), ('6.8', '6.8'), ('7.0', '7.0'), ('7.2', '7.2'), ('7.6', '7.6'), ('N/A', 'N/A')], default='6.0', max_length=3)),
                ('high_range_ph', models.CharField(choices=[('7.4', '7.4'), ('7.8', '7.8'), ('8.0', '8.0'), ('8.2', '8.2'), ('8.4', '8.4'), ('8.8', '8.8'), ('N/A', 'N/A')], default='7.4', max_length=3)),
                ('ammonia', models.CharField(choices=[('0', '0'), ('0.25', '0.25'), ('0.5', '0.5'), ('1.0', '1.0'), ('2.0', '2.0'), ('4.0', '4.0'), ('8.0', '8.0'), ('N/A', 'N/A')], default='0', max_length=4)),
                ('nitrite', models.CharField(choices=[('0', '0'), ('0.25', '0.25'), ('0.5', '0.5'), ('1.0', '1.0'), ('2.0', '2.0'), ('5.0', '5.0'), ('N/A', 'N/A')], default='0', max_length=4)),
                ('nitrate', models.CharField(choices=[('0', '0'), ('5.0', '5.0'), ('10', '10'), ('20', '20'), ('40', '40'), ('80', '80'), ('160', '160'), ('N/A', 'N/A')], default='0', max_length=3)),
                ('aquarium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='water_quality_management.aquarium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
