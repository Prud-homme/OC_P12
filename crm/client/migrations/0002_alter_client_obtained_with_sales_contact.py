# Generated by Django 4.1.1 on 2022-10-13 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="obtained_with_sales_contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="client_obtained_with_sales_contact",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
