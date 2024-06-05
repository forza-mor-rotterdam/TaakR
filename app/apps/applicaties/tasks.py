import celery
from apps.applicaties.models import Applicatie
from apps.taaktypes.models import Taaktype
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

DEFAULT_RETRY_DELAY = 2
MAX_RETRIES = 6

LOCK_EXPIRE = 5


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    max_retries = MAX_RETRIES
    default_retry_delay = DEFAULT_RETRY_DELAY


@shared_task(bind=True, base=BaseTaskWithRetry)
def fetch_and_save_taaktypes(self, applicatie_id):
    try:
        applicatie = Applicatie.objects.get(id=applicatie_id)
        taaktypes = applicatie.taaktypes_halen()
        print(f"Taaktypes: {taaktypes}")
        save_taaktypes(applicatie, taaktypes)
        logger.info(f"Fetched and saved taaktypes for {applicatie.naam}")
    except Applicatie.DoesNotExist:
        logger.error(f"Applicatie with id {applicatie_id} does not exist")
    except Exception as e:
        logger.error(f"Error fetching taaktypes for Applicatie id {applicatie_id}: {e}")


def save_taaktypes(applicatie, taaktypes):
    for taaktype_data in taaktypes:
        print(f"Taaktype data: {taaktype_data}")
        Taaktype.objects.update_or_create(
            taakapplicatie_taaktype_url=taaktype_data.get("_links", {}).get("self"),
            taakapplicatie=applicatie,
            actief=taaktype_data.get("actief", True),
            defaults={
                "omschrijving": taaktype_data.get("omschrijving", ""),
            },
        )
