# Generated by Django 4.1.4 on 2023-07-12 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_app', '0006_employee_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='emergency',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='language',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='salary',
        ),
    ]
