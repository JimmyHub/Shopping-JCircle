from .models import ShoppingList
from rest_framework import serializers

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingList
        fields = "__all__"
