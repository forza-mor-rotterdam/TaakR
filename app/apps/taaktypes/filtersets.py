import logging

from apps.taaktypes.models import Afdeling, Taaktype
from django.forms.fields import CharField, MultipleChoiceField, URLField
from django_filters import rest_framework as filters

logger = logging.getLogger(__name__)


class MultipleValueField(MultipleChoiceField):
    def __init__(self, *args, field_class, **kwargs):
        self.inner_field = field_class()
        super().__init__(*args, **kwargs)

    def valid_value(self, value):
        return self.inner_field.validate(value)

    def clean(self, values):
        return values and [self.inner_field.clean(value) for value in values]


class MultipleValueFilter(filters.Filter):
    field_class = MultipleValueField

    def __init__(self, *args, field_class, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, field_class=field_class, **kwargs)


class TaaktypeFilter(filters.FilterSet):
    taakapplicatie_taaktype_url = MultipleValueFilter(
        field_class=CharField, method="get_taakapplicatie_taaktype_urls"
    )
    actief = filters.BooleanFilter(method="get_actief")

    def get_taakapplicatie_taaktype_urls(self, queryset, name, value):
        if value:
            return queryset.filter(taakapplicatie_taaktype_url__in=value).distinct()
        return queryset

    def get_actief(self, queryset, name, value):
        return queryset.filter(actief=value)

    class Meta:
        model = Taaktype
        fields = [
            "taakapplicatie_taaktype_url",
        ]


class AfdelingFilter(filters.FilterSet):
    taakapplicatie_basis_url = MultipleValueFilter(
        field_class=URLField, method="get_taakapplicatie_basis_url"
    )
    taaktype_actief = filters.BooleanFilter(method="get_taaktype_actief")

    def get_taakapplicatie_basis_url(self, queryset, name, value):
        if value:
            return queryset.filter(
                taaktypes_voor_afdelingen__taakapplicatie__basis_url__in=value
            ).distinct()
        return queryset

    def get_taaktype_actief(self, queryset, name, value):
        return queryset.filter(taaktypes_voor_afdelingen__actief=value)

    class Meta:
        model = Afdeling
        fields = []
