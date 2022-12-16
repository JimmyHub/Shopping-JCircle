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
        carts = self.queryset.filter(user=request.user.username)
        if not carts:
            result = {'code': status.HTTP_200_OK, 'error': 'This shoppingcart is empty'}
            return JsonResponse(result)
        data = []
        for i in carts:
            dic_cart = {
                'list_id': i.id,
                'pname': i.product.pname,
                'pid': i.product.id,
                'pkind': i.product.pkind,
                'pphoto': str(i.product.pphoto),
                'price': i.product.pprice,
                'count': i.count,
            }
            data.append(dic_cart)
        result = {'code': 200, 'data': data}
        return Response(data=result)

    # 購物車加入
    def create(self, request, keyword):
        data_cart = get_json_data(request.body)
        product = get_object_or_404(ProductProfile, id=keyword)
        get_serializer_data(self, data_cart)
        product_exsist = get_object_or_404(self.queryset, product_id=product.id)

        # 判斷購物車內是否已經有此商品,有的話 將數量加上
        if product_exsist:
            product_exsist.count = product_exsist.count + self.serializer.validated_data['count']
            product_exsist.save()
        # 若購物車內還沒有此商品就加入購物車
        else:
            self.serializer.validated_data['product'] = product_exsist
            self.serializer.validated_data['user'] = request.user
            self.serializer.create(self.serializer.validated_data)
        result = {'code': 200}
        return Response(data=result)

    # 購物車修改
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)

        carts = get_object_or_404(self.queryset, id=pk)
        carts[0].count = int(data['count'])
        carts[0].save()
        result = {'code': status.HTTP_200_OK}
        return Response(data=result)

    # 購物車刪除
    def destroy(self, request, pk=None):
        cart = get_object_or_404(self.queryset, id=pk)
        if cart:
            if cart.user.username == request.user.username:
                cart.delete()
                result = {'code': status.HTTP_200_OK}
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'Who are you ?'}
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'Something must be wrong'}
        return Response(data=result)
