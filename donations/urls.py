from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from donations.api.views import CollectViewSet, PaymentViewSet
from config.urls import schema_view

router = DefaultRouter()
router.register(r"collects", CollectViewSet, basename="collect")
router.register(r"payments", PaymentViewSet, basename="payment")


urlpatterns = [
    # Основные API эндпоинты
    path("api/", include(router.urls)),
    # Документация Swagger/OpenAPI
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
