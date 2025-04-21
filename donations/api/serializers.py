from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model

from donations.models import Collect, Payment

User = get_user_model()


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для модели Payment:
    - Используется HyperlinkedModelSerializer для REST-навигации
    - Поля, генерируемые автоматически, установлены как только для чтения
    - В create() автоматически устанавливается текущий пользователь как донор
    """
    url = serializers.HyperlinkedIdentityField(view_name='payment-detail')
    donator = serializers.StringRelatedField(read_only=True)
    collect = serializers.HyperlinkedRelatedField(
        view_name='collect-detail',
        queryset=Collect.objects.all()
    )

    class Meta:
        model = Payment
        fields = ['url', 'id', 'collect', 'donator', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at', 'donator']

    def create(self, validated_data):
        """
        Устанавливает текущего пользователя
        как донора перед созданием объекта Payment
        """
        user = self.context['request'].user
        validated_data['donator'] = user
        return super().create(validated_data)


class CollectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для модели Collect:
    - Используется HyperlinkedModelSerializer для REST-навигации
    - Включает вложенные платежи только для чтения
    - Поля, рассчитываемые или устанавливаемые автоматически,
    сделаны только для чтения
    - Реализована валидация бизнес-правил
    """
    url = serializers.HyperlinkedIdentityField(view_name='collect-detail')
    author = serializers.StringRelatedField(read_only=True)
    cover_image = serializers.ImageField(required=False)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = [
            'url', 'id', 'author', 'title', 'reason', 'description',
            'cover_image', 'goal_amount', 'is_infinite',
            'collected_amount', 'donators_count', 'ends_at',
            'created_at', 'payments'
        ]
        read_only_fields = [
            'id', 'created_at', 'author', 'collected_amount', 'donators_count'
        ]

    def validate(self, attrs):
        """
        Проверка бизнес-логики:
        - Если сбор не бесконечный, должна быть указана цель (goal_amount)
        - Дата окончания (ends_at) должна быть в будущем
        """
        is_infinite = attrs.get(
            'is_infinite', getattr(self.instance, 'is_infinite', False)
        )
        goal = attrs.get(
            'goal_amount', getattr(self.instance, 'goal_amount', None)
        )
        if not is_infinite and goal is None:
            raise serializers.ValidationError(
                "Если 'is_infinite' установлено в False,"
                "необходимо указать 'goal_amount'."
            )

        ends_at = attrs.get('ends_at', getattr(self.instance, 'ends_at', None))
        if ends_at and ends_at <= timezone.now():
            raise serializers.ValidationError(
                "Поле 'ends_at' должно быть указано как дата/время в будущем."
            )
        return attrs

    def create(self, validated_data):
        """
        Устанавливает текущего пользователя
        как автора перед созданием объекта Collect
        """
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
