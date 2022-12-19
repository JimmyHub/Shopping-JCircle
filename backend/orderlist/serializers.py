from rest_framework import serializers

from shoppingcart.models import ShoppingList

from .models import OrderList


class OrderListSerializer(serializers.Serializer):
    # 訂單編號
    num_list = serializers.IntegerField()
    # 商品數量
    counts = serializers.ListField()
    # 商品id
    products = serializers.ListField()
    # 購物車id
    list_id = serializers.ListField()

    def create(self, validated_data):
        counts = validated_data['counts']
        products = validated_data['products']
        for i in range(len(validated_data['counts'])):
            OrderList.objects.create(count=counts[i],
                                     product_id=products[i],
                                     num_list_id=validated_data['num_list'], )
        for sid in validated_data['list_id']:
            shoppingcart = ShoppingList.objects.filter(id=sid)
            shoppingcart[0].delete()