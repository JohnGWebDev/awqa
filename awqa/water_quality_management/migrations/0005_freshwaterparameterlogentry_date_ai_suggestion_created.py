# Generated by Django 5.1.1 on 2024-12-04 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_quality_management', '0004_freshwaterparameterlogentry_openai_token_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='freshwaterparameterlogentry',
            name='date_ai_suggestion_created',
            field=models.DateTimeField(null=True),
        ),
    ]
