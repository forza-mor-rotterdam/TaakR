from apps.bijlagen.models import Bijlage
from apps.taaktypes.models import (
    Afdeling,
    Link,
    Taaktype,
    TaaktypeMiddel,
    TaaktypeVoorbeeldsituatie,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.reverse import reverse


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "url",
            "titel",
            "toon_in_planr",
            "toon_in_taakapplicatie",
            "open_in_nieuwe_tab",
        )


class TaaktypeLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()
    taakapplicatie_taaktype_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_self(self, obj):
        return reverse(
            "v1:taaktype-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )

    @extend_schema_field(OpenApiTypes.URI)
    def get_taakapplicatie_taaktype_url(self, obj):
        return obj.taakapplicatie_taaktype_url


class TaaktypeSerializer(serializers.ModelSerializer):
    _links = TaaktypeLinksSerializer(source="*")
    afdelingen = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:afdeling-detail",
        lookup_field="uuid",
    )
    verantwoordelijke_afdeling = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name="v1:afdeling-detail",
        lookup_field="uuid",
    )
    taaktypemiddelen = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:taaktype_middel-detail",
        lookup_field="uuid",
    )
    volgende_taaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:taaktype-detail",
        lookup_field="uuid",
    )
    gerelateerde_taaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:taaktype-detail",
        lookup_field="uuid",
    )
    voorbeeldsituatie_voor_taaktype = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:taaktype_voorbeeldsituatie-detail",
        lookup_field="uuid",
    )
    links = LinkSerializer(
        many=True,
        source="links_voor_taaktype",
    )

    class Meta:
        model = Taaktype
        fields = (
            "_links",
            "uuid",
            # "taakapplicatie_taaktype_uuid",
            "omschrijving",
            "toelichting",
            "verantwoordelijke_afdeling",
            "icoon",
            "additionele_informatie",
            "actief",
            "afdelingen",
            "taaktypemiddelen",
            "volgende_taaktypes",
            "gerelateerde_taaktypes",
            "gerelateerde_onderwerpen",
            "voorbeeldsituatie_voor_taaktype",
            "taakapplicatie_taaktype_url",
            "links",
        )
        read_only_fields = ("_links",)


class AfdelingLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_self(self, obj):
        return reverse(
            "v1:afdeling-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )


class AfdelingSerializer(serializers.ModelSerializer):
    _links = AfdelingLinksSerializer(source="*")
    taaktypes_voor_afdelingen = TaaktypeSerializer(many=True, read_only=True)

    class Meta:
        model = Afdeling
        fields = (
            "_links",
            "uuid",
            "naam",
            "onderdeel",
            "icoon",
            "taaktypes_voor_afdelingen",
        )


class TaaktypeMiddelLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_self(self, obj):
        return reverse(
            "v1:taaktype_middel-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )


class TaaktypeMiddelSerializer(serializers.ModelSerializer):
    _links = TaaktypeMiddelLinksSerializer(source="*")

    class Meta:
        model = TaaktypeMiddel
        fields = (
            "_links",
            "uuid",
            "naam",
        )


class TaaktypeVoorbeeldsituatieLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()
    taaktype = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.URI)
    def get_self(self, obj):
        return reverse(
            "v1:taaktype_voorbeeldsituatie-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )

    @extend_schema_field(OpenApiTypes.URI)
    def get_taaktype(self, obj):
        return reverse(
            "v1:taaktype-detail",
            kwargs={"uuid": obj.taaktype.uuid},
            request=self.context.get("request"),
        )


class BijlagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bijlage
        fields = (
            "afbeelding",
            "afbeelding_verkleind",
        )


class TaaktypeVoorbeeldsituatieSerializer(serializers.ModelSerializer):
    _links = TaaktypeVoorbeeldsituatieLinksSerializer(source="*")
    bijlagen = BijlagenSerializer(many=True)

    class Meta:
        model = TaaktypeVoorbeeldsituatie
        fields = (
            "_links",
            "uuid",
            "toelichting",
            "type",
            "bijlagen",
        )
