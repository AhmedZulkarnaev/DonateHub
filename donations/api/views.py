from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from donations.models import Collect, Payment
from api.serializers import CollectSerializer, PaymentSerializer


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
