import logging
from urllib.parse import urlencode, urlparse

import requests
import urllib3
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from requests import Request, Response
from utils.models import BasisModel

logger = logging.getLogger(__name__)


def encrypt_gebruiker_wachtwoord(wachtwoord_decrypted):
    f = Fernet(settings.FERNET_KEY)
    try:
        wachtwoord_encrypted = f.encrypt(wachtwoord_decrypted.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption with fernet key error: {e}")
    return wachtwoord_encrypted


class Applicatie(BasisModel):
    """
    Representeerd externe applicaite die de afhandling van de melden op zich nemen.
    """

    naam = models.CharField(
        max_length=100,
        default="Applicatie",
    )
    basis_url = models.URLField(default="https://example.com")
    valide_basis_urls = ArrayField(
        base_field=models.URLField(),
        default=list,
    )
    taaktype_aanmaken_formulier_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.naam

    class ApplicationAuthResponseException(Exception):
        ...

    class ApplicatieBasisUrlFout(Exception):
        ...

    class ApplicatieWerdNietGevondenFout(Exception):
        ...

    class NotificatieVoorApplicatieFout(Exception):
        ...

    class TaaktypesOphalenFout(Exception):
        ...

    class AntwoordFout(Exception):
        ...

    @classmethod
    def vind_applicatie_obv_uri(cls, uri):
        url_o = urlparse(uri)
        applicatie = Applicatie.objects.filter(
            basis_url=f"{url_o.scheme}://{url_o.netloc}"
        ).first()
        if not applicatie:
            applicatie = Applicatie.objects.filter(
                valide_basis_urls__contains=[f"{url_o.scheme}://{url_o.netloc}"]
            ).first()
        if not applicatie:
            logger.warning(f"Er is geen Applicatie gevonden bij deze url: url={uri}")
        return applicatie

    def _get_timeout(self):
        return (10, 20)

    def _get_url(self, url):
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            nieuwe_url = f"{self.basis_url}{url}"
            return nieuwe_url
        if (
            f"{url_o.scheme}://{url_o.netloc}" == self.basis_url
            or f"{url_o.scheme}://{url_o.netloc}" in self.valide_basis_urls
        ):
            nieuwe_url = (
                f"{self.basis_url}{url_o.path}{'?' if url_o.query else ''}{url_o.query}"
            )
            return nieuwe_url
        raise Applicatie.ApplicatieBasisUrlFout(
            f"url: {url}, basis_url: {self.basis_url}"
        )

    def _get_headers(self):
        return {
            "user-agent": urllib3.util.SKIP_HEADER,
        }

    def _do_request(
        self, url, method="get", data={}, params={}, raw_response=True, cache_timeout=0
    ):
        action: Request = getattr(requests, method)
        url = self._get_url(url)
        action_params: dict = {
            "url": url,
            "headers": self._get_headers(),
            "json": data,
            "params": params,
            "timeout": self._get_timeout(),
        }
        if cache_timeout and method == "get":
            cache_key = f"{url}?{urlencode(params)}"
            response = cache.get(cache_key)
            if not response:
                try:
                    response: Response = action(**action_params)
                except Exception as e:
                    logger.error(f"error: {e}")
                    raise Applicatie.AntwoordFout(
                        f"Er is iets mis gegaan met de verbinding tussen TaakR en {self.naam}"
                    )
                if int(response.status_code) == 200:
                    cache.set(cache_key, response, cache_timeout)
        else:
            try:
                response: Response = action(**action_params)
            except Exception as e:
                logger.error(f"error: {e}")
                raise Applicatie.AntwoordFout(
                    f"Er is iets mis gegaan met de verbinding tussen TaakR en {self.naam}"
                )
        if raw_response:
            return response
        return response.json()

    def taaktypes_halen(self, cache_timeout=60):
        if self.basis_url:
            taaktypes_response = self._do_request(
                "/api/v1/taaktype/",
                params={"limit": 200},
                method="get",
                cache_timeout=cache_timeout,
            )
            if taaktypes_response.status_code == 200:
                return taaktypes_response.json().get("results", [])
            if taaktypes_response.status_code == 404:
                error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}"
            elif taaktypes_response.status_code != 200:
                try:
                    error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}, antwoord={taaktypes_response.json().get('detail', taaktypes_response.json())}"
                except Exception:
                    error = f"De taaktypes voor {self.naam} konden niet worden opgehaald: fout code={taaktypes_response.status_code}"
                logger.error(error)
                raise Applicatie.TaaktypesOphalenFout(error)

        else:
            error = f"taaktypes voor applicatie '{self.naam}' konden niet worden opgehaald: basis_url ontbreekt"
        logger.error(error)
        return []

    def fetch_taaktype_data(self, url):
        try:
            response = self._do_request(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching taaktype data from {url}: {e}")
            return None
