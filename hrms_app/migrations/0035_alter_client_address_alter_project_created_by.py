# Generated by Django 4.2.3 on 2023-08-01 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hrms_app", "0034_project_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="address",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
