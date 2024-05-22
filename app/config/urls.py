from apps.aliassen.viewsets import OnderwerpAliasViewSet
from apps.applicaties.viewsets import TaakapplicatieViewSet
from apps.authenticatie.views import GetGebruikerAPIView, SetGebruikerAPIView
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
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django_db_schema_renderer.urls import schema_urls
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
router.register(r"bijlage", BijlageViewSet, basename="bijlage")

urlpatterns = [
    path("api/v1/", include((router.urls, "app"), namespace="v1")),
    path(
        "api/v1/gebruiker/<str:email>/",
        GetGebruikerAPIView.as_view(),
        name="get_gebruiker",
    ),
    path("api/v1/gebruiker/", SetGebruikerAPIView.as_view(), name="set_gebruiker"),
    path("api-token-auth/", views.obtain_auth_token),
    path("login/", login_required_view, name="login_required"),
    path("health/", include("health_check.urls")),
    path("healthz/", healthz, name="healthz"),
    path("db-schema/", include((schema_urls, "db-schema"))),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
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
    re_path(r"^media", serve_protected_media, name="protected_media"),
]

if settings.OIDC_ENABLED:
    urlpatterns += [
        path("oidc/", include("mozilla_django_oidc.urls")),
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
