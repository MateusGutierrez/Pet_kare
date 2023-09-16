# Generated by Django 4.2.3 on 2023-07-31 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trait",
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
                ("name", models.CharField(max_length=20, unique=True)),
                ("pets", models.ManyToManyField(related_name="traits", to="pets.pet")),
            ],
        ),
    ]
