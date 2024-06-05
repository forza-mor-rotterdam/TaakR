import logging

from apps.applicaties.models import Applicatie
from apps.applicaties.tasks import fetch_and_save_taaktypes
from django.contrib import admin, messages

logger = logging.getLogger(__name__)


class TaakapplicatieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "naam",
    )
    actions = ["fetch_taaktypes"]

    def fetch_taaktypes(self, request, queryset):
        for applicatie in queryset:
            fetch_and_save_taaktypes.delay(applicatie.id)
        self.message_user(request, "Taaktypes fetching has been started.")

    fetch_taaktypes.short_description = "Fetch and save taaktypes"

    def save_model(self, request, obj, form, change):
        try:
            if obj.taaktypes_halen(cache_timeout=0):
                messages.success(request, "Connectie met de applicatie is gelukt")
            else:
                messages.error(request, "Connectie met de applicatie is mislukt!")
        except Exception:
            messages.error(request, "Connectie met de applicatie is mislukt!")

        obj.save()


admin.site.register(Applicatie, TaakapplicatieAdmin)
