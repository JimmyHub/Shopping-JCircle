from .models import OrdersFiles
from rest_framework import serializers

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrdersFiles
        fields = "__all__"
