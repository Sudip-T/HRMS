# Generated by Django 4.1.4 on 2023-07-14 03:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_app', '0017_alter_leave_number_of_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leave_reason',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
