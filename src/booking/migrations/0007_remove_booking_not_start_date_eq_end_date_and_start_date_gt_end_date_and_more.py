# Generated by Django 4.2.17 on 2025-01-16 12:46

import django.contrib.postgres.constraints
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0006_auto_20250116_1218"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="booking",
            name="not_start_date_eq_end_date_and_start_date_gt_end_date",
        ),
        migrations.RemoveField(
            model_name="car",
            name="description",
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(
                expressions=[
                    ("car", "="),
                    (models.Func(models.F("start_date"), models.F("end_date"), function="DATERANGE"), "&&"),
                ],
                name="prevent_overlapping_bookings",
            ),
        ),
    ]
