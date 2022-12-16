from rest_framework import serializers

from user.serializers import UserSerializer

from .models import ProductProfile


class ProductBaseSerializer(serializers.ModelSerializer):
    pname = serializers.CharField(max_length=50)
    pkind = serializers.CharField(max_length=30)
    pcontent = serializers.CharField(required=False)
    pprice = serializers.IntegerField(min_value=0)

    class Meta:
        model = ProductProfile
        fields = ("pname", "pkind", "pcontent", "pprice")

    def create(self, validated_data):
        product_exist = ProductProfile.objects.filter(pname=validated_data['pname'])
        if not product_exist:
            return ProductProfile.objects.create(**validated_data)
        else:
            for p in product_exist:
                if p.sales_id == validated_data['sales'].username:
                    raise SystemError("商品名稱已存在")


class ProductSerializer(ProductBaseSerializer):
    pphoto = serializers.ImageField(use_url='product/')

    class Meta:
        model = ProductProfile
        fields = ("pname", "pkind", "pcontent", "pprice", "pphoto")

    def update(self, instance, data):
        product_queryset = ProductProfile.objects.filter(pname=data['pname'])
        for p in product_queryset:
            if p.sales_id == data['user'].username:
                raise SystemError("商品名稱已存在")
        return ProductProfile.objects.filter(pk=instance.id).update(**data)
