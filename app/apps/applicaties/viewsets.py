from apps.applicaties.models import Applicatie
from apps.applicaties.serializers import TaakapplicatieSerializer
from rest_framework import viewsets


class TaakapplicatieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Taakapplicaties voor TaakR
    """

    lookup_field = "uuid"
    queryset = Applicatie.objects.all()
    permission_classes = ()
    serializer_class = TaakapplicatieSerializer
