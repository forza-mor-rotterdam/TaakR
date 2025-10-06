import logging

from apps.authenticatie.forms import GebruikerAanmakenForm, GebruikerAanpassenForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

logger = logging.getLogger(__name__)
Gebruiker = get_user_model()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.has_perms(["authorisatie.beheer_bekijken"]):
            return redirect(reverse("beheer"))
        if request.user.is_authenticated:
            return redirect(reverse("taaktype_lijst"), False)

        if settings.OIDC_ENABLED:
            return redirect(f"/oidc/authenticate/?next={request.GET.get('next', '/')}")
        if settings.ENABLE_DJANGO_ADMIN_LOGIN:
            return redirect(f"/admin/login/?next={request.GET.get('next', '/admin')}")

        return HttpResponse("Er is geen login ingesteld")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"), False)

        if settings.OIDC_ENABLED:
            return redirect("/oidc/logout/")
        if settings.ENABLE_DJANGO_ADMIN_LOGIN:
            return redirect(f"/admin/logout/?next={request.GET.get('next', '/')}")

        return HttpResponse("Er is geen logout ingesteld")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.gebruiker_bekijken", raise_exception=True),
    name="dispatch",
)
class GebruikerView(View):
    model = Gebruiker
    success_url = reverse_lazy("gebruiker_lijst")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.gebruiker_lijst_bekijken", raise_exception=True),
    name="dispatch",
)
class GebruikerLijstView(GebruikerView, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = self.object_list.prefetch_related("groups")
        context["geauthoriseerde_gebruikers"] = object_list.filter(groups__isnull=False)
        context["ongeauthoriseerde_gebruikers"] = object_list.filter(
            groups__isnull=True
        )
        return context


class GebruikerAanmakenAanpassenView(GebruikerView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.clear()
        if form.cleaned_data.get("group"):
            self.object.groups.add(form.cleaned_data.get("group"))
        return response


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.gebruiker_aanpassen", raise_exception=True),
    name="dispatch",
)
class GebruikerAanpassenView(GebruikerAanmakenAanpassenView, UpdateView):
    form_class = GebruikerAanpassenForm
    template_name = "authenticatie/gebruiker_aanpassen.html"

    def get_initial(self):
        initial = self.initial.copy()
        obj = self.get_object()
        initial["group"] = obj.groups.all().first()
        return initial


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.gebruiker_aanmaken", raise_exception=True),
    name="dispatch",
)
class GebruikerAanmakenView(GebruikerAanmakenAanpassenView, CreateView):
    template_name = "authenticatie/gebruiker_aanmaken.html"
    form_class = GebruikerAanmakenForm
