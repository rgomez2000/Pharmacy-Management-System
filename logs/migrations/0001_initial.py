# Generated by Django 5.1.1 on 2024-10-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrescriptionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmacist_name', models.CharField(max_length=100)),
                ('prescription_number', models.CharField(max_length=50)),
                ('patient_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('drug_type', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
