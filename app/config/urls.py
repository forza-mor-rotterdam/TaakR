from apps.aliassen.viewsets import OnderwerpAliasViewSet
from apps.applicaties.viewsets import TaakapplicatieViewSet
from apps.authenticatie.views import (
    GebruikerAanmakenView,
    GebruikerAanpassenView,
    GebruikerLijstView,
)
from apps.authenticatie.viewsets import GetGebruikerAPIView, SetGebruikerAPIView
from apps.authorisatie.views import (
    RechtengroepAanmakenView,
    RechtengroepAanpassenView,
    RechtengroepLijstView,
    RechtengroepVerwijderenView,
)
from apps.beheer.views import beheer
from apps.bijlagen.viewsets import BijlageViewSet
from apps.health.views import healthz
from apps.main.views import (
    clear_melding_token_from_cache,
    config,
    http_403,
    http_404,
    http_500,
    login_required_view,
    root,
    serve_protected_media,
    ui_settings_handler,
)
from apps.taaktypes.views import (
    AfdelingAanmakenView,
    AfdelingAanpassenView,
    AfdelingLijstView,
    TaaktypeAanmakenView,
    TaaktypeAanpassenView,
    TaaktypeDetailView,
    TaaktypeLijstView,
    TaaktypeMiddelAanmakenView,
    TaaktypeMiddelAanpassenView,
    TaaktypeMiddelLijstView,
)
from apps.taaktypes.viewsets import (
    AfdelingViewSet,
    TaaktypeMiddelViewSet,
    TaaktypeViewSet,
    TaaktypeVoorbeeldsituatieViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django_db_schema_renderer.urls import schema_urls
from django_select2 import urls as select2_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"onderwerp-alias", OnderwerpAliasViewSet, basename="onderwerp-alias")
router.register(r"applicatie", TaakapplicatieViewSet, basename="applicatie")
router.register(r"taakapplicatie", TaakapplicatieViewSet, basename="taakapplicatie")
router.register(r"taaktype", TaaktypeViewSet, basename="taaktype")
router.register(r"afdeling", AfdelingViewSet, basename="afdeling")
router.register(r"taaktype-middel", TaaktypeMiddelViewSet, basename="taaktype_middel")
router.register(
    r"taaktype-voorbeeldsituatie",
    TaaktypeVoorbeeldsituatieViewSet,
    basename="taaktype_voorbeeldsituatie",
)
router.register(r"bijlage", BijlageViewSet, basename="bijlage")


urlpatterns = [
    path("", root, name="root"),
    path("api/v1/", include((router.urls, "app"), namespace="v1")),
    path(
        "api/v1/gebruiker/<str:email>/",
        GetGebruikerAPIView.as_view(),
        name="get_gebruiker",
    ),
    path("api/v1/gebruiker/", SetGebruikerAPIView.as_view(), name="set_gebruiker"),
    path("api-token-auth/", views.obtain_auth_token),
    path("config/", config, name="config"),
    path("health/", include("health_check.urls")),
    path("healthz/", healthz, name="healthz"),
    path("db-schema/", include((schema_urls, "db-schema"))),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # START beheer
    path("beheer/", beheer, name="beheer"),
    path("beheer/gebruiker/", GebruikerLijstView.as_view(), name="gebruiker_lijst"),
    path(
        "beheer/gebruiker/aanmaken/",
        GebruikerAanmakenView.as_view(),
        name="gebruiker_aanmaken",
    ),
    path(
        "beheer/gebruiker/<int:pk>/aanpassen/",
        GebruikerAanpassenView.as_view(),
        name="gebruiker_aanpassen",
    ),
    path(
        "beheer/rechtengroep/",
        RechtengroepLijstView.as_view(),
        name="rechtengroep_lijst",
    ),
    path(
        "beheer/rechtengroep/aanmaken/",
        RechtengroepAanmakenView.as_view(),
        name="rechtengroep_aanmaken",
    ),
    path(
        "beheer/rechtengroep/<int:pk>/aanpassen/",
        RechtengroepAanpassenView.as_view(),
        name="rechtengroep_aanpassen",
    ),
    path(
        "beheer/rechtengroep/<int:pk>/verwijderen/",
        RechtengroepVerwijderenView.as_view(),
        name="rechtengroep_verwijderen",
    ),
    path("beheer/taaktype/", TaaktypeLijstView.as_view(), name="taaktype_lijst"),
    path(
        "beheer/taaktype/aanmaken/",
        TaaktypeAanmakenView.as_view(),
        name="taaktype_aanmaken",
    ),
    path(
        "beheer/taaktype/<int:pk>/",
        TaaktypeDetailView.as_view(),
        name="taaktype_detail",
    ),
    path(
        "beheer/taaktype/<int:pk>/aanpassen/",
        TaaktypeAanpassenView.as_view(),
        name="taaktype_aanpassen",
    ),
    path("beheer/afdeling/", AfdelingLijstView.as_view(), name="afdeling_lijst"),
    path(
        "beheer/afdeling/aanmaken/",
        AfdelingAanmakenView.as_view(),
        name="afdeling_aanmaken",
    ),
    path(
        "beheer/afdeling/<int:pk>/aanpassen/",
        AfdelingAanpassenView.as_view(),
        name="afdeling_aanpassen",
    ),
    path(
        "beheer/taaktypemiddel/",
        TaaktypeMiddelLijstView.as_view(),
        name="taaktypemiddel_lijst",
    ),
    path(
        "beheer/taaktypemiddel/aanmaken/",
        TaaktypeMiddelAanmakenView.as_view(),
        name="taaktypemiddel_aanmaken",
    ),
    path(
        "beheer/taaktypemiddel/<int:pk>/aanpassen/",
        TaaktypeMiddelAanpassenView.as_view(),
        name="taaktypemiddel_aanpassen",
    ),
    # START partials
    path("part/pageheader-form/", ui_settings_handler, name="pageheader_form_part"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("select2/", include(select2_urls)),
]

if settings.OIDC_ENABLED:
    urlpatterns += [
        path(
            "admin/login/",
            RedirectView.as_view(
                url="/oidc/authenticate/?next=/admin/",
                permanent=False,
            ),
            name="admin_login",
        ),
        path(
            "admin/logout/",
            RedirectView.as_view(
                url="/oidc/logout/?next=/admin/",
                permanent=False,
            ),
            name="admin_logout",
        ),
    ]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
]

if settings.APP_ENV != "productie":
    urlpatterns += [
        path("403/", http_403, name="403"),
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
