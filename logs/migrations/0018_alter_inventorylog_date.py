# Generated by Django 5.1.1 on 2024-11-24 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0017_druglog_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventorylog",
            name="date",
            field=models.DateField(),
        ),
    ]
