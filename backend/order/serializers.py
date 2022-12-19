from rest_framework import serializers

from .models import OrdersFiles


class OrderSerializer(serializers.Serializer):
    num_list = serializers.IntegerField()
    num_time = serializers.CharField()
    status = serializers.IntegerField()
    gname = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=60)
    phone = serializers.CharField(max_length=11)
    payway = serializers.IntegerField()
    content = serializers.CharField(max_length=60)
    bonus = serializers.IntegerField()
    shipping = serializers.IntegerField()
    money_total = serializers.IntegerField()

    def create(self, validated_data):
        return OrdersFiles.objects.create(**validated_data)
