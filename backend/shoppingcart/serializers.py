from rest_framework import serializers

from .models import ShoppingList


class ShopSerializer(serializers.Serializer):
    count = serializers.IntegerField()

    def create(self, validated_data):
        return ShoppingList.objects.create(**validated_data)
