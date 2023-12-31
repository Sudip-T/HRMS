# Generated by Django 4.2.3 on 2023-08-01 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hrms_app", "0030_delete_mymodel_alter_employee_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emppersonalinfo",
            name="marital_status",
            field=models.CharField(
                choices=[
                    ("Married", "Married"),
                    ("Single", "Single"),
                    ("Divorced", "Divorced"),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[
                    ("New", "New"),
                    ("Pending", "PENDING"),
                    ("Working", "WORKING"),
                    ("Completed", "Completed"),
                ],
                default="New",
                max_length=10,
                null=True,
            ),
        ),
    ]
