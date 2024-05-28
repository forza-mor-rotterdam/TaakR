import logging
from urllib.parse import urlparse

from apps.services.basis import BasisService
from django.conf import settings
from django.template.loader import get_template
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


def render_onderwerp(onderwerp_url, standaar_naam=None):
    onderwerp = OnderwerpenService().get_onderwerp(onderwerp_url)
    standaard_naam = onderwerp.get(
        "name", "Niet gevonden!" if not standaar_naam else standaar_naam
    )
    if onderwerp.get("priority") == "high":
        spoed_badge = get_template("badges/spoed.html")
        return mark_safe(f"{standaard_naam}{spoed_badge.render()}")
    return standaard_naam


class OnderwerpenService(BasisService):
    _api_base_url = None
    _timeout: tuple[int, ...] = (5, 10)
    _api_path: str = "/api/v1"

    class BasisUrlFout(Exception):
        ...

    class DataOphalenFout(Exception):
        ...

    def __init__(self, *args, **kwargs: dict):
        self._api_base_url = settings.ONDERWERPEN_URL
        super().__init__(*args, **kwargs)

    def get_url(self, url):
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            return f"{self._api_base_url}{url}"
        if f"{url_o.scheme}://{url_o.netloc}" == self._api_base_url:
            return url
        raise OnderwerpenService.BasisUrlFout(
            f"url: {url}, basis_url: {self._api_base_url}"
        )

    def get_onderwerp(self, url) -> dict:
        return self.do_request(url, cache_timeout=60 * 10, raw_response=False)

    def get_groep(self, group_uuid) -> dict:
        return self.do_request(
            f"{self._api_base_url}{self._api_path}/group/{group_uuid}",
            cache_timeout=60 * 10,
            raw_response=False,
        )

    def get_onderwerpen(self) -> dict:
        return self.do_request(
            f"{self._api_base_url}{self._api_path}/category?limit=1000",
            cache_timeout=60 * 10,
            raw_response=False,
        )
