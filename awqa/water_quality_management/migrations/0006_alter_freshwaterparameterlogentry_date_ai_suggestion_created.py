# Generated by Django 5.1.1 on 2024-12-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_quality_management', '0005_freshwaterparameterlogentry_date_ai_suggestion_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freshwaterparameterlogentry',
            name='date_ai_suggestion_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]