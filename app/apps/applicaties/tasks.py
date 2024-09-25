import celery
from apps.applicaties.models import Applicatie
from apps.taaktypes.models import Taaktype
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

DEFAULT_RETRY_DELAY = 2
MAX_RETRIES = 1


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    max_retries = MAX_RETRIES
    default_retry_delay = DEFAULT_RETRY_DELAY


@shared_task(bind=True, base=BaseTaskWithRetry)
def fetch_and_save_taaktypes(self, applicatie_id):
    applicatie = Applicatie.objects.get(id=applicatie_id)
    taaktypes = applicatie.taaktypes_halen()
    logger.info(f"Taaktypes: {taaktypes}")
    save_taaktypes.delay(applicatie, taaktypes)
    logger.info(f"Fetched and saved taaktypes for {applicatie.naam}")


@shared_task(bind=True, base=BaseTaskWithRetry)
def save_taaktypes(applicatie, taaktypes):
    for taaktype_data in taaktypes:
        save_taaktype.delay(applicatie, taaktype_data)


@shared_task(bind=True, base=BaseTaskWithRetry)
def save_taaktype(applicatie, taaktype_data):
    logger.info(f"Taaktype data: {taaktype_data}")
    url = taaktype_data.get("_links", {}).get("self")
    if isinstance(url, dict):
        url = url.get("href")

    taaktype, created = Taaktype.objects.update_or_create(
        taakapplicatie_taaktype_url=url,
        defaults={
            "taakapplicatie": applicatie,
            "actief": taaktype_data.get("actief", True),
            "omschrijving": taaktype_data.get("omschrijving", ""),
            "toelichting": taaktype_data.get("toelichting", ""),
        },
    )
    if created:
        logger.info(
            f"Created new Taaktype {taaktype.uuid} with for taakapplicatie taaktype with url: {url}"
        )
    else:
        logger.info(
            f"Updated Taaktype {taaktype.uuid} with for taakapplicatie taaktype with url: {url}"
        )
