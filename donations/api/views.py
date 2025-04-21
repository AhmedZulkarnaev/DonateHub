from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from donations.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from ..cache import cache_response
from ..constants import CACHE_KEY_PREFIX


class CollectViewSet(ModelViewSet):
    """
    ViewSet для модели Collect:
    - Поддерживает полный CRUD через REST API
    - Только авторизованные пользователи могут создавать/изменять/удалять
    - Неавторизованные пользователи могут только просматривать
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(key_prefix=f"{CACHE_KEY_PREFIX}_single")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для модели Payment:
    - Поддерживает CRUD операции для платежей
    - Только авторизованные пользователи могут отправлять платежи
    - Неавторизованные пользователи могут только просматривать
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @cache_response(key_prefix=CACHE_KEY_PREFIX)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(key_prefix=f"{CACHE_KEY_PREFIX}_single")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
