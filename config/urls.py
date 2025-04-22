from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="API documentation for your project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("donations.urls")),
    # Регистрация
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # Документация Swagger/OpenAPI
    path("swagger/", schema_view.as_view(), name="swagger-docs"),
]
