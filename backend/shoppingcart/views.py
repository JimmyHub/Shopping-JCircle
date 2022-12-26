from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Store.tool import get_json_data, get_serializer_data
from Store.decorator import allmethods, trycatch, request_response
from Store.authentication import TokenExAuthentication
from product.models import ProductProfile

from .models import ShoppingList
from .serializers import ShopSerializer


@allmethods(trycatch)
class ShoppingViewSet(GenericViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = [TokenExAuthentication, ]

    # 購物車瀏覽
    def list(self, request):
        carts = self.queryset.filter(user_id=request.user.username)
        if not carts:
            result = {'code': status.HTTP_200_OK, 'data': []}
            return Response(data=result)
        data = []
        cart_total = 0
        for i in carts:
            dic_cart = {
                'list_id': i.id,
                'pname': i.product.pname,
                'pid': i.product.id,
                'pkind': i.product.pkind,
                'pphoto': str(i.product.pphoto),
                'pprice': i.product.pprice,
                'count': i.count,
                'sales': i.product.sales_id,
                'total_price': i.product.pprice * i.count
            }
            cart_total += dic_cart['total_price']
            data.append(dic_cart)
        result = {'code': 200, 'data': data, 'cart_total': cart_total}
        return Response(data=result)

    # 購物車加入
    def create(self, request, keyword):
        data_cart = get_json_data(request.body)
        product = get_object_or_404(ProductProfile, id=keyword)
        get_serializer_data(self, data_cart)
        product_exsist = self.queryset.filter(product_id=product.id).filter(user_id=request.user.username)

        # 判斷購物車內是否已經有此商品,有的話 將數量加上
        if product_exsist:
            product_exsist[0].count = int(product_exsist[0].count) + self.serializer.validated_data['count']
            product_exsist[0].save()
        # 若購物車內還沒有此商品就加入購物車
        else:
            self.serializer.validated_data['product_id'] = product.id
            self.serializer.validated_data['user_id'] = request.user.username
            self.serializer.create(self.serializer.validated_data)
        result = {'code': 200}
        return Response(data=result)

    # 購物車修改
    def partial_update(self, request, keyword=None):
        data = get_json_data(request.body)

        carts = get_object_or_404(self.queryset, id=keyword)
        carts.count = int(data['count'])
        carts.save()
        result = {'code': status.HTTP_200_OK}
        return Response(data=result)

    # 購物車刪除
    def destroy(self, request, keyword=None):
        cart = self.queryset.filter(user_id =request.user.username).filter(product_id=keyword)
        if cart:
            cart[0].delete()
            result = {'code': status.HTTP_200_OK}
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': '購物車內無此商品'}
        return Response(data=result)
