# Generated by Django 4.1.1 on 2022-09-16 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=25)),
                ("lastname", models.CharField(max_length=25)),
                ("email", models.EmailField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                ("mobile", models.CharField(max_length=20)),
                ("company_name", models.CharField(max_length=250)),
                ("date_created", models.DateTimeField(editable=False)),
                ("date_updated", models.DateTimeField(editable=False)),
                (
                    "sales_contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_sales_contact",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
