# Generated by Django 5.1.1 on 2024-10-26 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0001_initial'),
        ('med_inventory', '0002_rename_quantity_medication_stock_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_qty', models.PositiveIntegerField(default=0)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='drugs.drug')),
            ],
            options={
                'permissions': [('can_check_inventory', 'Can check inventory')],
            },
        ),
        migrations.DeleteModel(
            name='Medication',
        ),
    ]
