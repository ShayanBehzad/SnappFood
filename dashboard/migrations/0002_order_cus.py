# Generated by Django 4.2.7 on 2024-03-08 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("custapi", "0001_initial"),
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="cus",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="custapi.customer",
            ),
        ),
    ]
