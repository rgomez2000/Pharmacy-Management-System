# Generated by Django 5.1.1 on 2024-11-24 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cashier", "0008_alter_receipt_transaction_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="transaction_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 11, 24, 19, 44, 52, 314279, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
