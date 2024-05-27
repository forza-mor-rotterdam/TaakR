import logging

from apps.applicaties.models import Applicatie
from apps.applicaties.tasks import fetch_and_save_taaktypes
from django.contrib import admin, messages
from django.core.cache import cache

logger = logging.getLogger(__name__)


class TaakapplicatieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "naam",
        "gebruiker",
    )
    actions = ["fetch_taaktypes"]

    def fetch_taaktypes(self, request, queryset):
        for applicatie in queryset:
            fetch_and_save_taaktypes.delay(applicatie.id)
        self.message_user(request, "Taaktypes fetching has been started.")

    fetch_taaktypes.short_description = "Fetch and save taaktypes"

    def save_model(self, request, obj, form, change):
        if obj.pk:
            cache.delete(obj.get_token_cache_key())
            orig_obj = Applicatie.objects.get(pk=obj.pk)
            if (
                obj.applicatie_gebruiker_wachtwoord
                != orig_obj.applicatie_gebruiker_wachtwoord
            ):
                try:
                    obj.encrypt_applicatie_gebruiker_wachtwoord(
                        obj.applicatie_gebruiker_wachtwoord
                    )
                except Exception as e:
                    logger.error(f"Encryption error: {e}, obj pk: {obj.pk}")

        elif obj.applicatie_gebruiker_wachtwoord:
            try:
                obj.encrypt_applicatie_gebruiker_wachtwoord(
                    obj.applicatie_gebruiker_wachtwoord
                )
            except Exception as e:
                logger.error(f"Encryption error: {e}")

        try:
            if obj._get_token():
                messages.success(request, "Connectie met de applicatie is gelukt")
            else:
                messages.error(request, "Connectie met de applicatie is mislukt!")
        except Exception:
            messages.error(request, "Connectie met de applicatie is mislukt!")

        obj.save()


admin.site.register(Applicatie, TaakapplicatieAdmin)
