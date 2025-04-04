from django.contrib.gis.db import models


class BasisPermissie:
    naam = None
    codenaam = None


class GebruikerLijstBekijkenPermissie(BasisPermissie):
    naam = "Gebruiker lijst bekijken"
    codenaam = "gebruiker_lijst_bekijken"


class GebruikerAanmakenPermissie(BasisPermissie):
    naam = "Gebruiker aanmaken"
    codenaam = "gebruiker_aanmaken"


class GebruikerBekijkenPermissie(BasisPermissie):
    naam = "Gebruiker bekijken"
    codenaam = "gebruiker_bekijken"


class GebruikerAanpassenPermissie(BasisPermissie):
    naam = "Gebruiker aanpassen"
    codenaam = "gebruiker_aanpassen"


class GebruikerVerwijderenPermissie(BasisPermissie):
    naam = "Gebruiker verwijderen"
    codenaam = "gebruiker_verwijderen"


class BeheerBekijkenPermissie(BasisPermissie):
    naam = "Beheer bekijken"
    codenaam = "beheer_bekijken"


class TaaktypeAanmakenPermissie(BasisPermissie):
    naam = "Taaktype aanmaken"
    codenaam = "taaktype_aanmaken"


class TaaktypeAanpassenPermissie(BasisPermissie):
    naam = "Taaktype aanpassen"
    codenaam = "taaktype_aanpassen"


class TaaktypeMiddelLijstBekijkenPermissie(BasisPermissie):
    naam = "Taaktypemiddel lijst bekijken"
    codenaam = "taaktypemiddel_lijst_bekijken"


class TaaktypeMiddelAanmakenPermissie(BasisPermissie):
    naam = "Taaktypemiddel aanmaken"
    codenaam = "taaktypemiddel_aanmaken"


class TaaktypeMiddelBekijkenPermissie(BasisPermissie):
    naam = "Taaktypemiddel bekijken"
    codenaam = "taaktypemiddel_bekijken"


class TaaktypeMiddelAanpassenPermissie(BasisPermissie):
    naam = "Taaktypemiddel aanpassen"
    codenaam = "taaktypemiddel_aanpassen"


class AfdelingLijstBekijkenPermissie(BasisPermissie):
    naam = "Afdeling lijst bekijken"
    codenaam = "afdeling_lijst_bekijken"


class AfdelingAanmakenPermissie(BasisPermissie):
    naam = "Afdeling aanmaken"
    codenaam = "afdeling_aanmaken"


class AfdelingBekijkenPermissie(BasisPermissie):
    naam = "Afdeling bekijken"
    codenaam = "afdeling_bekijken"


class AfdelingAanpassenPermissie(BasisPermissie):
    naam = "Afdeling aanpassen"
    codenaam = "afdeling_aanpassen"


class RechtengroepLijstBekijkenPermissie(BasisPermissie):
    naam = "Rechtengroep lijst bekijken"
    codenaam = "rechtengroep_lijst_bekijken"


class RechtengroepAanmakenPermissie(BasisPermissie):
    naam = "Rechtengroep aanmaken"
    codenaam = "rechtengroep_aanmaken"


class RechtengroepBekijkenPermissie(BasisPermissie):
    naam = "Rechtengroep bekijken"
    codenaam = "rechtengroep_bekijken"


class RechtengroepAanpassenPermissie(BasisPermissie):
    naam = "Rechtengroep aanpassen"
    codenaam = "rechtengroep_aanpassen"


class RechtengroepVerwijderenPermissie(BasisPermissie):
    naam = "Rechtengroep verwijderen"
    codenaam = "rechtengroep_verwijderen"


class VerantwoordelijkePersoonBekijkenPermissie(BasisPermissie):
    naam = "Verantwoordelijke persoon bekijken"
    codenaam = "verantwoordelijke_persoon_bekijken"


gebruikersgroep_permissies = (
    GebruikerLijstBekijkenPermissie,
    GebruikerAanmakenPermissie,
    GebruikerAanpassenPermissie,
    GebruikerBekijkenPermissie,
    GebruikerVerwijderenPermissie,
    BeheerBekijkenPermissie,
    TaaktypeAanmakenPermissie,
    TaaktypeAanpassenPermissie,
    TaaktypeMiddelLijstBekijkenPermissie,
    TaaktypeMiddelAanmakenPermissie,
    TaaktypeMiddelBekijkenPermissie,
    TaaktypeMiddelAanpassenPermissie,
    AfdelingLijstBekijkenPermissie,
    AfdelingAanmakenPermissie,
    AfdelingBekijkenPermissie,
    AfdelingAanpassenPermissie,
    RechtengroepLijstBekijkenPermissie,
    RechtengroepAanmakenPermissie,
    RechtengroepBekijkenPermissie,
    RechtengroepAanpassenPermissie,
    RechtengroepVerwijderenPermissie,
    VerantwoordelijkePersoonBekijkenPermissie,
)

gebruikersgroep_permissie_opties = [
    (p.codenaam, p.naam) for p in gebruikersgroep_permissies
]
permissie_namen = {p.codenaam: p.naam for p in gebruikersgroep_permissies}


class Permissie(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = gebruikersgroep_permissie_opties
