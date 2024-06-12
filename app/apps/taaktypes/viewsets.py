from apps.taaktypes.filtersets import AfdelingFilter, TaaktypeFilter
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
from django_filters import rest_framework as filters
from rest_framework import viewsets


class AfdelingViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Afdeling.objects.all().order_by("naam")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AfdelingFilter
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaaktypeFilter
    permission_classes = ()
    serializer_class = TaaktypeSerializer
