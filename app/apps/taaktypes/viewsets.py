from apps.applicaties.tasks import fetch_and_save_taaktypes
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
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema(
    parameters=[
        OpenApiParameter(
            "taakapplicatie_basis_url", OpenApiTypes.URI, OpenApiParameter.QUERY
        ),
        OpenApiParameter("taaktype_actief", OpenApiTypes.BOOL, OpenApiParameter.QUERY),
    ]
)
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

    @extend_schema(
        description="Vernieuw taaktypes",
        request={},
        responses={status.HTTP_200_OK: {}},
        parameters=[
            OpenApiParameter(
                "taakapplicatie_taaktype_url", OpenApiTypes.URI, OpenApiParameter.QUERY
            ),
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="vernieuw",
        serializer_class=TaaktypeSerializer,
    )
    def vernieuw(self, request):
        from apps.applicaties.models import Applicatie

        applicatie = Applicatie.vind_applicatie_obv_uri(
            request.GET.get("taakapplicatie_taaktype_url")
        )
        if applicatie:
            fetch_and_save_taaktypes.delay(applicatie.id)
            return Response({}, status=status.HTTP_200_OK)
        return Response(
            {"Deze url is niet bij ons bekend!"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
