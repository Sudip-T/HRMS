# Generated by Django 4.2.3 on 2023-07-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrms_app", "0023_remove_employee_mobile_employee_contact_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="birthday",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="employee",
            name="date_joined",
            field=models.DateField(),
        ),
    ]
