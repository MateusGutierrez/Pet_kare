# Generated by Django 4.2.3 on 2023-08-01 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trait",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
