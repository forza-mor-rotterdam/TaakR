import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication

logger = logging.getLogger(__name__)


def http_403(request):
    return render(
        request,
        "403.html",
    )


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


# Verander hier de instellingen voor de nieuwe homepagina.
@login_required
def root(request):
    if request.user.has_perms(["authorisatie.beheer_bekijken"]):
        return redirect(reverse("beheer"), False)
    return render(
        request,
        "home.html",
        {},
    )


@login_required
def ui_settings_handler(request):
    return render(
        request,
        "snippets/form_pageheader.html",
    )


@user_passes_test(lambda u: u.is_superuser)
def clear_melding_token_from_cache(request):
    cache.delete("meldingen_token")
    return HttpResponse("melding_token removed from cache")


@login_required
def config(request):
    return render(
        request,
        "config.html",
    )


@login_required
def login_required_view(request):
    return HttpResponseRedirect(redirect_to="/admin/")


def serve_protected_media(request):
    user = TokenAuthentication().authenticate(request)
    if user or settings.ALLOW_UNAUTHORIZED_MEDIA_ACCESS:
        url = request.path.replace("media", "media-protected")
        response = HttpResponse("")
        response["X-Accel-Redirect"] = url
        response["Content-Type"] = ""
        return response
    return HttpResponseForbidden()
