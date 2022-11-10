from .models import OrderList
from rest_framework import serializers

class OrderListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderList
        fields = "__all__"
