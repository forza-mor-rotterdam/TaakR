import logging

from apps.applicaties.models import Applicatie
from apps.bijlagen.models import Bijlage
from apps.bijlagen.tasks import task_aanmaken_afbeelding_versies
from apps.taaktypes.forms import (
    AfdelingAanmakenForm,
    AfdelingAanpassenForm,
    TaaktypeAanpassenForm,
    TaaktypeMiddelAanmakenForm,
    TaaktypeMiddelAanpassenForm,
    TaaktypeVoorbeeldsituatieNietFormSet,
    TaaktypeVoorbeeldsituatieWelFormSet,
)
from apps.taaktypes.models import (
    Afdeling,
    Taaktype,
    TaaktypeMiddel,
    TaaktypeVoorbeeldsituatie,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

logger = logging.getLogger(__name__)


class TaaktypeView(View):
    model = Taaktype
    success_url = reverse_lazy("taaktype_lijst")


class TaaktypeLijstView(TaaktypeView, ListView):
    queryset = Taaktype.objects.prefetch_related(
        "volgende_taaktypes",
        "afdelingen",
        "taaktypemiddelen",
        "voorbeeldsituatie_voor_taaktype",
        "voorbeeldsituatie_voor_taaktype__bijlagen",
    ).order_by("omschrijving")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["afdeling_onderdelen"] = [
            [
                onderdeel[1],
                self.queryset.filter(
                    afdelingen__onderdeel=onderdeel[0], actief=True
                ).distinct(),
            ]
            for onderdeel in Afdeling.OnderdeelOpties.choices
        ]
        context["zonder_afdeling"] = self.queryset.filter(
            Q(Q(afdelingen__isnull=True) | Q(afdelingen__onderdeel__isnull=True)),
            actief=True,
        ).distinct()

        context["niet_actief"] = self.queryset.filter(
            actief=False,
        ).distinct()

        for taaktype in context["afdeling_onderdelen"]:
            taaktype_list = taaktype[1]
            for t in taaktype_list:
                t.voorbeeld_wel = None
                for voorbeeld in t.voorbeeldsituatie_voor_taaktype.filter(
                    type="waarom_wel"
                ):
                    if voorbeeld.bijlagen.exists():
                        t.voorbeeld_wel = voorbeeld.bijlagen.first()
                        break

        for t in context["zonder_afdeling"]:
            t.voorbeeld_wel = None
            for voorbeeld in t.voorbeeldsituatie_voor_taaktype.filter(
                type="waarom_wel"
            ):
                if voorbeeld.bijlagen.exists():
                    t.voorbeeld_wel = voorbeeld.bijlagen.first()
                    break

        context["applicaties"] = Applicatie.objects.all()
        context[
            "editable"
        ] = self.request.user.is_authenticated and self.request.user.has_perms(
            ["authorisatie.taaktype_aanpassen"]
        )

        return context


class TaaktypeDetailView(TaaktypeView, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "editable"
        ] = self.request.user.is_authenticated and self.request.user.has_perms(
            ["authorisatie.taaktype_aanpassen"]
        )
        return context


@method_decorator(login_required, name="dispatch")
class TaaktypeAanmakenAanpassenView(TaaktypeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset_wel = TaaktypeVoorbeeldsituatie.objects.filter(
            type=TaaktypeVoorbeeldsituatie.TypeOpties.WAAROM_WEL,
            taaktype=self.object,
        )
        queryset_niet = TaaktypeVoorbeeldsituatie.objects.filter(
            type=TaaktypeVoorbeeldsituatie.TypeOpties.WAAROM_NIET,
            taaktype=self.object,
        )
        TaaktypeVoorbeeldsituatieWelFormSet.extra = 5 - queryset_wel.count()
        TaaktypeVoorbeeldsituatieNietFormSet.extra = 5 - queryset_niet.count()

        if self.request.POST:
            context["voorbeeldsituatie_wel"] = TaaktypeVoorbeeldsituatieWelFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix="voorbeeldsituatie_wel",
                queryset=queryset_wel,
            )
            context["voorbeeldsituatie_niet"] = TaaktypeVoorbeeldsituatieNietFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix="voorbeeldsituatie_niet",
                queryset=queryset_niet,
            )
        else:
            context["voorbeeldsituatie_wel"] = TaaktypeVoorbeeldsituatieWelFormSet(
                instance=self.object,
                prefix="voorbeeldsituatie_wel",
                queryset=queryset_wel,
            )
            context["voorbeeldsituatie_niet"] = TaaktypeVoorbeeldsituatieNietFormSet(
                instance=self.object,
                prefix="voorbeeldsituatie_niet",
                queryset=queryset_niet,
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save()
        formsets = [context["voorbeeldsituatie_wel"], context["voorbeeldsituatie_niet"]]
        if not all([x.is_valid() for x in formsets]):
            return self.render_to_response(self.get_context_data(form=form))

        for voorbeeldsituatie_formset in [
            context["voorbeeldsituatie_wel"],
            context["voorbeeldsituatie_niet"],
        ]:
            voorbeeldsituaties = voorbeeldsituatie_formset.save(commit=False)
            for obj in voorbeeldsituatie_formset.deleted_objects:
                obj.delete()
            for voorbeeldsituatie in voorbeeldsituaties:
                voorbeeldsituatie.taaktype = self.object
                voorbeeldsituatie.save()
            for form in voorbeeldsituatie_formset.forms:
                if hasattr(form.files, "getlist") and form.files.getlist(
                    f"{form.prefix}-bestand"
                ):
                    bijlagen = [
                        Bijlage(
                            content_object=form.instance,
                            bestand=bijlage,
                        )
                        for bijlage in form.files.getlist(f"{form.prefix}-bestand")
                    ]
                    aangemaakte_bijlages = Bijlage.objects.bulk_create(bijlagen)
                    for bijlage in aangemaakte_bijlages:
                        task_aanmaken_afbeelding_versies.delay(bijlage.pk)

                form.bijlage_formset.save(commit=False)
                for bijlage in form.bijlage_formset.deleted_objects:
                    bijlage.delete()

        return redirect(reverse("taaktype_aanpassen", args=[self.object.id]))


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktype_aanpassen", raise_exception=True),
    name="dispatch",
)
class TaaktypeAanpassenView(TaaktypeAanmakenAanpassenView, UpdateView):
    form_class = TaaktypeAanpassenForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_taaktype = self.get_object()
        kwargs["current_taaktype"] = current_taaktype
        return kwargs


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktype_aanmaken", raise_exception=True),
    name="dispatch",
)
class TaaktypeAanmakenView(View):
    def get(self, request, *args, **kwargs):
        applicatie = Applicatie.vind_applicatie_obv_uri(request.GET.get("taaktype_url"))
        if not applicatie:
            messages.error(request, "Dit is geen geldige taaktype url")
            return redirect(reverse("taaktype_lijst"))

        taaktype_data = applicatie.fetch_taaktype_data(request.GET.get("taaktype_url"))
        logger.info(f"TaaktypeAanmakenView: {taaktype_data}")
        taaktype, aangemaakt = Taaktype.objects.update_or_create(
            taakapplicatie_taaktype_url=taaktype_data.get("_links", {}).get("self"),
            defaults={
                "taakapplicatie_taaktype_uuid": taaktype_data.get("uuid"),
                "taakapplicatie": applicatie,
                "actief": taaktype_data.get("actief", True),
                "omschrijving": taaktype_data.get("omschrijving", ""),
                "toelichting": taaktype_data.get("toelichting", ""),
            },
        )
        if aangemaakt:
            messages.success(
                request,
                f"Het taaktype '{taaktype.omschrijving}' is aangemaakt of aangepast in {applicatie.naam} en in TaakR",
            )
        return redirect(reverse("taaktype_aanpassen", args=[taaktype.id]))


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.afdeling_bekijken", raise_exception=True),
    name="dispatch",
)
class AfdelingView(View):
    model = Afdeling
    success_url = reverse_lazy("afdeling_lijst")
    queryset = Afdeling.objects.order_by("naam")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.afdeling_lijst_bekijken", raise_exception=True),
    name="dispatch",
)
class AfdelingLijstView(AfdelingView, ListView):
    ...


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.afdeling_bekijken", raise_exception=True),
    name="dispatch",
)
class AfdelingAanmakenAanpassenView(AfdelingView):
    ...


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.afdeling_aanpassen", raise_exception=True),
    name="dispatch",
)
class AfdelingAanpassenView(AfdelingAanmakenAanpassenView, UpdateView):
    form_class = AfdelingAanpassenForm


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.afdeling_aanmaken", raise_exception=True),
    name="dispatch",
)
class AfdelingAanmakenView(AfdelingAanmakenAanpassenView, CreateView):
    form_class = AfdelingAanmakenForm


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktypemiddel_bekijken", raise_exception=True),
    name="dispatch",
)
class TaaktypeMiddelView(View):
    model = TaaktypeMiddel
    success_url = reverse_lazy("taaktypemiddel_lijst")
    queryset = TaaktypeMiddel.objects.order_by("naam")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required(
        "authorisatie.taaktypemiddel_lijst_bekijken", raise_exception=True
    ),
    name="dispatch",
)
class TaaktypeMiddelLijstView(TaaktypeMiddelView, ListView):
    ...


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktypemiddel_bekijken", raise_exception=True),
    name="dispatch",
)
class TaaktypeMiddelAanmakenAanpassenView(TaaktypeMiddelView):
    ...


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktypemiddel_aanpassen", raise_exception=True),
    name="dispatch",
)
class TaaktypeMiddelAanpassenView(TaaktypeMiddelAanmakenAanpassenView, UpdateView):
    form_class = TaaktypeMiddelAanpassenForm


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.taaktypemiddel_aanmaken", raise_exception=True),
    name="dispatch",
)
class TaaktypeMiddelAanmakenView(TaaktypeMiddelAanmakenAanpassenView, CreateView):
    form_class = TaaktypeMiddelAanmakenForm
