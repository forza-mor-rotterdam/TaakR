# Generated by Django 4.2.11 on 2024-06-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taaktypes", "0003_alter_taaktype_taakapplicatie_taaktype_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="taaktype",
            name="taakapplicatie_taaktype_uuid",
            field=models.UUIDField(null=True, unique=True),
        ),
    ]