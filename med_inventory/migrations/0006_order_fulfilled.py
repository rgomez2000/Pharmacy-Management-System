# Generated by Django 5.1.1 on 2024-11-10 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_inventory', '0005_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fulfilled',
            field=models.BooleanField(default=False),
        ),
    ]
