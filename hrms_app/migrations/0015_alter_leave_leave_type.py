# Generated by Django 4.1.4 on 2023-07-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_app', '0014_leave_leave_type_alter_leave_end_alter_leave_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='leave_type',
            field=models.CharField(choices=[('Causal Leave', 'CAUSAL'), ('Emergency Leave', 'EMERGENCY'), ('Sick Leave', 'SICK')], max_length=50),
        ),
    ]
