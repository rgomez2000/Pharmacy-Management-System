# Generated by Django 5.1.1 on 2024-11-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashier", "0005_receipt_pharmacy_address_receipt_pharmacy_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="pharmacy_address",
            field=models.TextField(default="1209 E 2nd St #100"),
        ),
        migrations.AlterField(
            model_name="receipt",
            name="pharmacy_phone",
            field=models.CharField(default="(520) 855-3010", max_length=20),
        ),
    ]