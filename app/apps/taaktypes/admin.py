from apps.applicaties.tasks import fetch_and_save_taaktypes
from apps.taaktypes.models import (
    Afdeling,
    Taaktype,
    TaaktypeMiddel,
    TaaktypeVoorbeeldsituatie,
)
from django.contrib import admin


class AfdelingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "naam",
        "onderdeel",
    )
    list_editable = ("naam", "onderdeel")


class TaaktypeMiddelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "naam",
    )
    list_editable = ("naam",)


class TaaktypeAdmin(admin.ModelAdmin):
    list_display = ("taakapplicatie", "taakapplicatie_taaktype_url", "omschrijving")
    search_fields = ("taakapplicatie__naam", "omschrijving")
    actions = ["refresh_taaktypes"]
    list_filter = ("taakapplicatie",)

    def refresh_taaktypes(self, request, queryset):
        applicatie_ids = queryset.values_list("taakapplicatie_id", flat=True).distinct()
        for applicatie_id in applicatie_ids:
            fetch_and_save_taaktypes.delay(applicatie_id)
        self.message_user(request, "Taaktypes refresh has been started.")

    refresh_taaktypes.short_description = "Refresh selected taaktypes"


class TaaktypeVoorbeeldsituatieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "taaktype",
        "toelichting",
    )


admin.site.register(Afdeling, AfdelingAdmin)
admin.site.register(TaaktypeMiddel, TaaktypeMiddelAdmin)
admin.site.register(TaaktypeVoorbeeldsituatie, TaaktypeVoorbeeldsituatieAdmin)
admin.site.register(Taaktype, TaaktypeAdmin)
