# Generated by Django 4.1.7 on 2023-03-01 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='users.venueownerprofile'),
        ),
    ]
