# Generated by Django 5.1.1 on 2024-11-24 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashier", "0006_alter_receipt_pharmacy_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="transaction_date",
            field=models.DateTimeField(),
        ),
    ]
