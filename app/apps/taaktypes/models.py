from apps.bijlagen.models import Bijlage
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from utils.models import BasisModel

### Future code below ###


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

    taakapplicatie_taaktype_uuid = models.UUIDField(
        editable=True, unique=True, null=True
    )

    taakapplicatie = models.ForeignKey(
        to="applicaties.Applicatie",
        related_name="taaktypes_voor_applicatie",
        on_delete=models.CASCADE,
    )

    omschrijving = models.CharField(max_length=200)

    toelichting = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    verantwoordelijke = models.CharField(
        max_length=200,
        blank=True,
        null=True,
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


# Usable code from other apps below:

#     taaktype = Taaktype.objects.filter(id=vervolg_taak).first()
# taaktype_url = (
#     drf_reverse(
#         "v1:taaktype-detail",
#         kwargs={"uuid": taaktype.uuid},
#         request=request,
#     )
#     if taaktype
#     else None
# )

# def taaktype_namen(self):
#     taakapplicaties = MeldingenService().taakapplicaties().get("results", [])
#     taaktypes = [tt for ta in taakapplicaties for tt in ta.get("taaktypes", [])]
#     taaktype_namen = [
#         taaktype.get("omschrijving")
#         for taaktype in taaktypes
#         if urlparse(taaktype.get("_links", {}).get("self")).path
#         in [urlparse(tt).path for tt in self.taaktypes]
#     ]
#     return taaktype_namen

# def get_taaktypes(melding, request):
# from apps.context.utils import get_gebruiker_context

# gebruiker_context = get_gebruiker_context(request.user)

# taakapplicaties = MeldingenService(request=request).taakapplicaties()
# taaktypes = [
#     [
#         tt.get("_links", {}).get("self"),
#         f"{tt.get('omschrijving')}",
#     ]
#     for ta in taakapplicaties.get("results", [])
#     for tt in ta.get("taaktypes", [])
#     if urlparse(tt.get("_links", {}).get("self")).path
#     in [urlparse(tt).path for tt in gebruiker_context.taaktypes]
#     and tt.get("actief", False)
# ]
# gebruikte_taaktypes = [
#     *set(
#         list(
#             to.get("taaktype")
#             for to in melding.get("taakopdrachten_voor_melding", [])
#             if not to.get("resolutie")
#         )
#     )
# ]
# taaktypes = [tt for tt in taaktypes if tt[0] not in gebruikte_taaktypes]
# return taaktypes


# def taaktypes_halen(self, cache_timeout=60):
#     if self.basis_url:
#         taaktypes_response = self._do_request(
#             "/api/v1/taaktype/",
#             params={"limit": 200},
#             method="get",
#             cache_timeout=cache_timeout,
#         )
#         if taaktypes_response.status_code == 200:
#             return taaktypes_response.json().get("results", [])
#         if taaktypes_response.status_code == 404:
#             error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}"
#         elif taaktypes_response.status_code != 200:
#             try:
#                 error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}, antwoord={taaktypes_response.json().get('detail', taaktypes_response.json())}"
#             except Exception:
#                 error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}"
#             logger.error(error)
#             raise Applicatie.TaaktypesOphalenFout(error)

#     else:
#         error = f"taaktypes voor applicatie '{self.naam}' konden niet worden opgehaald: basis_url ontbreekt"
#     logger.error(error)
#     return []

# def fetch_taaktype_data(self, url):
#     try:
#         response = self._do_request(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         logger.error(f"Error fetching taaktype data from {url}: {e}")
#         return None
