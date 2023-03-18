# Generated by Django 4.1.7 on 2023-03-06 04:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventseattype',
            name='available_seats',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
