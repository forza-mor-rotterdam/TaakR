from apps.bijlagen.models import Bijlage
from apps.taaktypes.models import (
    Afdeling,
    Taaktype,
    TaaktypeMiddel,
    TaaktypeVoorbeeldsituatie,
)
from rest_framework import serializers
from rest_framework.reverse import reverse


class TaaktypeLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()

    def get_self(self, obj):
        return reverse(
            "v1:taaktype-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )


class TaaktypeSerializer(serializers.ModelSerializer):
    _links = TaaktypeLinksSerializer(source="*")
    # afdelingen = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name="v1:afdeling-detail",
    #     lookup_field="uuid",
    # )
    # taaktypemiddelen = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name="v1:taaktype_middel-detail",
    #     lookup_field="uuid",
    # )
    volgende_taaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="v1:taaktype-detail",
        lookup_field="uuid",
    )
    # gerelateerde_taaktypes = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name="v1:taaktype-detail",
    #     lookup_field="uuid",
    # )
    # voorbeeldsituatie_voor_taaktype = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name="v1:taaktype_voorbeeldsituatie-detail",
    #     lookup_field="uuid",
    # )

    class Meta:
        model = Taaktype
        fields = (
            "_links",
            "uuid",
            "omschrijving",
            "toelichting",
            "verantwoordelijke",
            "icoon",
            "additionele_informatie",
            "actief",
            # "afdelingen",
            # "taaktypemiddelen",
            "volgende_taaktypes",
            # "gerelateerde_taaktypes",
            "gerelateerde_onderwerpen",
            # "voorbeeldsituatie_voor_taaktype",
        )
        read_only_fields = ("_links",)


class AfdelingLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()

    def get_self(self, obj):
        return reverse(
            "v1:afdeling-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )


class AfdelingSerializer(serializers.ModelSerializer):
    _links = AfdelingLinksSerializer(source="*")

    class Meta:
        model = Afdeling
        fields = (
            "_links",
            "naam",
            "onderdeel",
        )


class TaaktypeMiddelLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()

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
            "naam",
        )


class TaaktypeVoorbeeldsituatieLinksSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField()
    taaktype = serializers.SerializerMethodField()

    def get_self(self, obj):
        return reverse(
            "v1:taaktype_voorbeeldsituatie-detail",
            kwargs={"uuid": obj.uuid},
            request=self.context.get("request"),
        )

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
            "toelichting",
            "type",
            "bijlagen",
        )
