# Generated by Django 5.1.1 on 2024-11-24 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashier", "0007_alter_receipt_transaction_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="transaction_date",
            field=models.DateTimeField(null=True),
        ),
    ]