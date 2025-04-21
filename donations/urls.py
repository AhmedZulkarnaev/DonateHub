from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from donations.api.views import CollectViewSet, PaymentViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'collects', CollectViewSet)
router.register(r'payments', PaymentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Donations API",
        default_version='v1',
        description="API for donation collections and payments",
        terms_of_service="https://your-terms-of-service.com/",
        contact=openapi.Contact(email="contact@donations.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
