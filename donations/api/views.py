from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from donations.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from ..cache import cache_response
from ..constants import CACHE_KEY_PREFIX


class CollectViewSet(ModelViewSet):
    """
    ViewSet для работы с денежными сборами (Collect).

    Позволяет:
    - Просматривать список сборов (GET /collects/)
    - Создавать новые сборы (POST /collects/)
    - Просматривать детали сбора (GET /collects/{id}/)
    - Обновлять сборы (PUT/PATCH /collects/{id}/)
    - Удалять сборы (DELETE /collects/{id}/)

    Требования:
    - Аутентификация требуется для создания, обновления и удаления
    - Анонимные пользователи могут только просматривать
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    @swagger_auto_schema(
        operation_description="Получить список всех денежных сборов",
        responses={200: CollectSerializer(many=True)},
        tags=['Сборы']
    )
    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о конкретном сборе",
        responses={
            200: CollectSerializer(),
            404: "Сбор не найден"
        },
        tags=['Сборы']
    )
    @cache_response(
        key_prefix=lambda view, request, *args, **kwargs:
        f"{CACHE_KEY_PREFIX}_single_{kwargs.get('pk') or kwargs.get('id')}")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый денежный сбор",
        request_body=CollectSerializer,
        responses={
            201: CollectSerializer(),
            400: "Неверные данные"
        },
        tags=['Сборы'],
        security=[{'Bearer': []}]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с платежами (Payment).

    Позволяет:
    - Просматривать список платежей (GET /payments/)
    - Создавать новые платежи (POST /payments/)
    - Просматривать детали платежа (GET /payments/{id}/)
    - Обновлять платежи (PUT/PATCH /payments/{id}/)
    - Удалять платежи (DELETE /payments/{id}/)

    Требования:
    - Аутентификация требуется для создания платежей
    - Анонимные пользователи могут только просматривать
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        operation_description="Получить список всех платежей",
        responses={200: PaymentSerializer(many=True)},
        tags=['Платежи']
    )
    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о конкретном платеже",
        responses={
            200: PaymentSerializer(),
            404: "Платеж не найден"
        },
        tags=['Платежи']
    )
    @cache_response(key_prefix=f"{CACHE_KEY_PREFIX}_single")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый платеж",
        request_body=PaymentSerializer,
        responses={
            201: PaymentSerializer(),
            400: "Неверные данные"
        },
        tags=['Платежи'],
        security=[{'Bearer': []}]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
