# Generated by Django 5.1.1 on 2024-11-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashier", "0009_alter_receipt_transaction_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="transaction_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
