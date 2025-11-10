from apps.bijlagen.models import Bijlage
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from utils.models import BasisModel

### Future code below ###


class Link(BasisModel):
    toon_in_planr = models.BooleanField(default=True)
    toon_in_taakapplicatie = models.BooleanField(default=True)
    open_in_nieuwe_tab = models.BooleanField(default=False)
    url = models.URLField()
    titel = models.CharField(max_length=100)
    taaktype = models.ForeignKey(
        to="taaktypes.Taaktype",
        related_name="links_voor_taaktype",
        on_delete=models.CASCADE,
    )


class Afdeling(BasisModel):
    """
    Afdeling model voor Taaktypes
    """

    class OnderdeelOpties(models.TextChoices):
        SHOON = "schoon", "Schoon"
        HEEL = "heel", "Heel"
        VELIG = "veilig", "Veilig"

    naam = models.CharField(max_length=100)
    onderdeel = models.CharField(
        max_length=50,
        choices=OnderdeelOpties.choices,
        null=True,
        blank=True,
    )
    icoon = models.ImageField(
        upload_to="afdeling/icons", null=True, blank=True, max_length=255
    )

    def __str__(self):
        return self.naam


class TaaktypeMiddel(BasisModel):
    """
    TaaktypeMiddel model voor Taaktypes
    """

    naam = models.CharField(max_length=100)

    def __str__(self):
        return self.naam


class TaaktypeVoorbeeldsituatie(BasisModel):
    """
    TaaktypeVoorbeeldsituatie model voor Taaktypes
    """

    class TypeOpties(models.TextChoices):
        WAAROM_WEL = "waarom_wel", "Waarom wel"
        WAAROM_NIET = "waarom_niet", "Waarom niet"

    toelichting = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=50,
        choices=TypeOpties.choices,
    )
    bijlagen = GenericRelation(Bijlage)

    taaktype = models.ForeignKey(
        to="taaktypes.Taaktype",
        related_name="voorbeeldsituatie_voor_taaktype",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.id}_{self.toelichting if self.toelichting else ''}"


class Taaktype(BasisModel):
    taakapplicatie_taaktype_url = models.URLField(
        unique=True
    )  # @TODO In endpoint moet dit in _links self zijn.

    taakapplicatie = models.ForeignKey(
        to="applicaties.Applicatie",
        related_name="taaktypes_voor_applicatie",
        on_delete=models.CASCADE,
    )

    omschrijving = models.CharField(max_length=200)

    toelichting = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
    )
    verantwoordelijke_afdeling = models.ForeignKey(
        to="taaktypes.Afdeling",
        related_name="verantwoordelijke_afdeling_taaktypes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    proceseigenaar_persoon_naam = models.CharField(
        verbose_name="Naam proceseigenaar",
        max_length=300,
        blank=True,
        null=True,
    )
    proceseigenaar_persoon_personeelsnummer = models.CharField(
        verbose_name="Personeelsnummer proceseigenaar",
        max_length=100,
        blank=True,
        null=True,
    )
    procesregiseur_persoon_naam = models.CharField(
        verbose_name="Naam procesregiseur",
        max_length=300,
        blank=True,
        null=True,
    )
    procesregiseur_persoon_personeelsnummer = models.CharField(
        verbose_name="Personeelsnummer procesregiseur",
        max_length=100,
        blank=True,
        null=True,
    )
    doorlooptijd = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
    )
    doorlooptijd_alleen_werkdagen = models.BooleanField(
        default=True,
    )
    icoon = models.ImageField(
        upload_to="taaktype/icons", null=True, blank=True, max_length=255
    )
    additionele_informatie = models.JSONField(default=dict)

    volgende_taaktypes = models.ManyToManyField(
        to="taaktypes.Taaktype",
        related_name="vorige_taaktypes_voor_taaktype",
        blank=True,
    )
    gerelateerde_taaktypes = models.ManyToManyField(
        to="taaktypes.Taaktype",
        related_name="gerelateerde_taaktypes_voor_taaktype",
        blank=True,
    )
    gerelateerde_onderwerpen = ArrayField(models.URLField(), default=list)
    afdelingen = models.ManyToManyField(
        to="taaktypes.Afdeling",
        related_name="taaktypes_voor_afdelingen",
        blank=True,
    )
    taaktypemiddelen = models.ManyToManyField(
        to="taaktypes.TaaktypeMiddel",
        related_name="taaktypes_voor_taaktypemiddelen",
        blank=True,
    )
    actief = models.BooleanField(default=True)

    def doorlooptijd_dagen_uren(self):
        uren_seconden = 60 * 60
        dagen_seconden = 24 * uren_seconden
        huidige_dagen_seconden = self.doorlooptijd - (
            self.doorlooptijd % dagen_seconden
        )
        huidige_uren_seconden = self.doorlooptijd - huidige_dagen_seconden
        dagen = int(huidige_dagen_seconden / dagen_seconden)
        uren = int(
            (huidige_uren_seconden - (huidige_uren_seconden % uren_seconden))
            / uren_seconden
        )

        periode = ""
        if dagen:
            periode += f"{dagen} {'dagen' if dagen > 1 else 'dag'}"
        if dagen and uren:
            periode += " en "
        if uren:
            periode += f"{uren} uur"
        return periode

    def bijlagen(self):
        return Bijlage.objects.filter(
            content_type=ContentType.objects.get_for_model(TaaktypeVoorbeeldsituatie),
            object_id__in=self.voorbeeldsituatie_voor_taaktype.values_list(
                "id", flat=True
            ),
        )

    class Meta:
        ordering = ("omschrijving",)
        verbose_name = "Taaktype"
        verbose_name_plural = "Taaktypes"

    def __str__(self) -> str:
        return f"{self.omschrijving}"
