# Generated by Django 4.1.7 on 2023-03-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0010_alter_venuecontact_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venuecontact',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
