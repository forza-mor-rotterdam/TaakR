# Generated by Django 3.2.19 on 2023-06-29 13:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OnderwerpAlias",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("aangemaakt_op", models.DateTimeField(auto_now_add=True)),
                ("aangepast_op", models.DateTimeField(auto_now=True)),
                ("bron_url", models.CharField(max_length=500)),
                (
                    "response_json",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
            options={
                "verbose_name": "Onderwerp alias",
                "verbose_name_plural": "Onderwerp aliassen",
            },
        ),
    ]
