# Generated by Django 4.1.4 on 2023-07-11 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_app', '0002_employee_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientpayment',
            name='payment_method',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
