# Generated by Django 4.1.7 on 2023-03-05 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_time_alter_event_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(),
        ),
    ]