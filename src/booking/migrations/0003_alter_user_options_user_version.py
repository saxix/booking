# Generated by Django 4.2.17 on 2024-12-21 11:59

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0002_alter_car_description_alter_car_services"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddField(
            model_name="user",
            name="version",
            field=concurrency.fields.AutoIncVersionField(
                default=0, help_text="record revision number"
            ),
        ),
    ]
