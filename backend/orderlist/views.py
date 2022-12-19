from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Store.tool import get_json_data, get_serializer_data
from Store.decorator import allmethods, trycatch, request_response
from Store.authentication import TokenExAuthentication
from order.models import OrdersFiles
from shoppingcart.models import ShoppingList

from .models import OrderList
from .serializers import OrderListSerializer


@allmethods(trycatch)
class OrderlistViewSet(GenericViewSet):
    queryset = OrderList.objects.all()
    serializer_class = OrderListSerializer
    authentication_classes = [TokenExAuthentication, ]

    def make_product_list(self, product_list, username, is_sales):
        list_tmp = []
        for i in product_list:
            target_name = i.product.sales.username if is_sales else i.num_list.buyer.username
            if username == target_name:
                dic_per_s = {
                    'pname': i.product.pname,
                    'id': i.product.id,
                    'photo': str(i.product.pphoto),
                    'price': i.product.pprice,
                    'count': i.count,
                }
                list_tmp.append(dic_per_s)
        return list_tmp

    # 訂單商品瀏覽
    def list(self, request, keyword=None, mode=None):
        products = self.queryset.filter(num_list_id=keyword)
        if not products:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'This list does not exist'}
            return Response(data=result)

        # 訂單商品資料總覽 直接寫在orders view裡面
        # mode =1 > 詳細訂單商品資料
        # 賣場詳細訂單商品顯示
        if mode == '1':
            list_products = self.make_product_list(products, request.user.username, True)
        elif mode == '0':
            list_products = self.make_product_list(products, request.user.username, False)
        else:
            list_products = []
        result = {'code': status.HTTP_200_OK, 'data': list_products}
        return Response(data=result)

    # 訂單商品創立
    def create(self, request):
        data_orderlist = get_json_data(request.body)
        get_serializer_data(self, data_orderlist)
        get_object_or_404(OrdersFiles, num_list=self.serializer.validated_data['num_list'])
        self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_200_OK, 'data': self.serializer.validated_data['num_list']}
        return Response(data=result)

    # 訂單商品刪除
    def destroy(self, request, keyword=None, mode=None):
        products = self.queryset.filter(num_list_id=keyword)
        for i in products:
            if request.user.username != i.num_list.buyer.username:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'you can not do this!'}
                return Response(data=result)
            else:
                # mode = 0 表示是在結帳時退回上一頁 刪除清單 要加回購物車
                if mode == '0':
                    ShoppingList.objects.create(
                        count=i.count,
                        product_id=i.product.id,
                        user_id=i.num_list.buyer.username)
                i.delete()

                # #mode = 1 表示是在我的訂單中刪除訂單 留言板 跟清單資料要先刪除
                # elif mode == '1':
                #     msgs= MessageRecord.objects.filter(num_list_id=keyword)
                #     if not msgs:
                #         continue
                #     else:
                #         for m in msgs:
                #             m.delete()
        result = {'code': status.HTTP_202_ACCEPTED}
        return Response(data=result)
