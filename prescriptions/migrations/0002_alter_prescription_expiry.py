# Generated by Django 5.1.1 on 2024-09-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prescriptions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescription",
            name="expiry",
            field=models.DateField(),
        ),
    ]