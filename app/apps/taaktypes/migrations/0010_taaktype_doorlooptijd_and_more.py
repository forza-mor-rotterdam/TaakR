# Generated by Django 4.2.15 on 2025-03-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taaktypes", "0009_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="taaktype",
            name="doorlooptijd",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="taaktype",
            name="doorlooptijd_alleen_werkdagen",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="taaktype",
            name="verantwoordelijke_persoon_naam",
            field=models.CharField(
                blank=True,
                max_length=300,
                null=True,
                verbose_name="Naam verantwoordelijke persoon",
            ),
        ),
        migrations.AddField(
            model_name="taaktype",
            name="verantwoordelijke_persoon_personeelsnummer",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Personeelsnummer verantwoordelijke persoon",
            ),
        ),
    ]
