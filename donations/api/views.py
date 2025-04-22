from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from donations.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from ..cache import cache_response
from ..constants import CACHE_KEY_PREFIX


class CollectViewSet(ModelViewSet):
    """
    API для управления денежными сборами:
    - Получить список: GET /collects/
    - Получить один сбор: GET /collects/{id}/
    - Создать сбор: POST /collects/
    - Обновить сбор: PUT/PATCH /collects/{id}/
    - Удалить сбор: DELETE /collects/{id}/
    """

    queryset = Collect.objects.filter(is_active=True)
    serializer_class = CollectSerializer

    @swagger_auto_schema(
        tags=["Сборы"], operation_description="Получить список всех сборов"
    )
    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Сборы"],
        operation_description="Получить информацию о конкретном сборе",
        responses={200: CollectSerializer},
    )
    @cache_response(
        key_prefix=lambda view, request, *args, **kwargs: f"{CACHE_KEY_PREFIX}_single_{kwargs.get('pk') or kwargs.get('id')}"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Сборы"],
        operation_description="Создать новый сбор",
        security=[{"Bearer": []}],
        responses={201: CollectSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentViewSet(ModelViewSet):
    """
    API для управления платежами:
    - Получить список: GET /payments/
    - Получить один платёж: GET /payments/{id}/
    - Создать платёж: POST /payments/
    - Обновить платёж: PUT/PATCH /payments/{id}/
    - Удалить платёж: DELETE /payments/{id}/
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        tags=["Платежи"], operation_description="Получить список всех платежей"
    )
    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Платежи"],
        operation_description="Получить информацию о конкретном платеже",
        responses={200: PaymentSerializer},
    )
    @cache_response(key_prefix=f"{CACHE_KEY_PREFIX}_single")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Платежи"],
        operation_description="Создать новый платёж",
        security=[{"Bearer": []}],
        responses={201: PaymentSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
