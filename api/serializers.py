from rest_framework import serializers
from donations.models import Collect, Payment


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Collect
        fields = [
            'id',
            'title',
            'reason',
            'description',
            'cover_image',
            'goal_amount',
            'is_infinite',
            'collected_amount',
            'donators_count',
            'ends_at',
            'created_at',
            'author',
        ]
        read_only_fields = [
            'collected_amount', 'donators_count', 'created_at', 'author'
        ]


class CollectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        exclude = [
            'collected_amount', 'donators_count', 'author', 'created_at'
            ]


class PaymentSerializer(serializers.ModelSerializer):
    donator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'collect', 'amount', 'donator', 'created_at']
        read_only_fields = ['donator', 'created_at']


class PaymentListSerializer(serializers.ModelSerializer):
    donator = PaymentSerializer()
    collect = CollectSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'created_at', 'donator', 'collect']
