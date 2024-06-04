from apps.taaktypes.models import (
    Afdeling,
    Taaktype,
    TaaktypeMiddel,
    TaaktypeVoorbeeldsituatie,
)
from apps.taaktypes.serializers import (
    AfdelingSerializer,
    TaaktypeMiddelSerializer,
    TaaktypeSerializer,
    TaaktypeVoorbeeldsituatieSerializer,
)
from rest_framework import viewsets


class AfdelingViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Afdeling.objects.all().order_by("naam")
    permission_classes = ()
    serializer_class = AfdelingSerializer


class TaaktypeMiddelViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = TaaktypeMiddel.objects.all().order_by("naam")
    permission_classes = ()
    serializer_class = TaaktypeMiddelSerializer


class TaaktypeVoorbeeldsituatieViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = TaaktypeVoorbeeldsituatie.objects.all()
    permission_classes = ()
    serializer_class = TaaktypeVoorbeeldsituatieSerializer


class TaaktypeViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Taaktype.objects.all()

    serializer_class = TaaktypeSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            return []
        return super().get_permissions()
