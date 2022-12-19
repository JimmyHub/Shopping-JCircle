from django.http import JsonResponse

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Store.tool import get_json_data, get_serializer_data
from Store.decorator import allmethods, trycatch, request_response
from Store.authentication import TokenExAuthentication
from user.models import UserProfile
from orderlist.models import OrderList
from Store.views import Ecpay
from .models import OrdersFiles
from .serializers import OrderSerializer


@allmethods(trycatch)
class OrdersViewSet(GenericViewSet):
    queryset = OrdersFiles.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenExAuthentication, ]

    # 訂單瀏覽
    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def list(self, request, keyword=None, mode=None):
        # 獲取訂單資料(不包含商品資料)
        if keyword == None:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'please give me keyword of list'}
            return JsonResponse(result)

        # keyword = 0 > 訂單總攬獲取
        if keyword == '0':
            # 賣場總覽獲取
            if mode == '1':
                order = self.queryset.filter(sales_id=request.user.username)
                list_orders = list(order.values('num_list', 'num_time', 'status', 'status_time', 'money_total')) if order else []
                # list_orders = list(self.queryset.filter(sales_id=request.user.username).values('num_list','num_time','status','status_time','money_total'))
            # 個人總覽獲取
            elif mode == '0':
                order = self.queryset.filter(buyer_id=request.user.username)
                list_orders = list(order.values('num_list', 'num_time', 'status', 'status_time', 'money_total')) if order else []
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'data': '訂單瀏覽模式錯誤'}
                return Response(data=result)

            if list_orders:
                for order in list_orders:
                    products_inOder = OrderList.objects.filter(num_list_id=order['num_list'])
                    order['products'] = (products_inOder[0].product.pname, products_inOder[0].count)
                result = {'code': status.HTTP_200_OK, 'data': list_orders}
            else:
                result = {'code': status.HTTP_200_OK, 'data': 'noorders'}
            return Response(data=result)

        else:
            # 訂單資料詳細顯示
            order = self.queryset.filter(num_list=keyword)
            order_data = list(order.values())
            order_data[0]['item'] = 'jCircle商品一組'
            order_data[0]['CheckMacValue'] = Ecpay.ecpay_jc(order_data[0]['num_list'])
            order_data[0]['num_show'] = 'jCircle' + str(order_data[0]['num_list'])
            result = {'code': status.HTTP_200_OK, 'data': order_data[0]}
            return Response(data=result)

    # 訂單創立
    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def create(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data)

        user = get_object_or_404(UserProfile, username=data.get('buyer', '')).username
        sale = get_object_or_404(UserProfile, username=data.get('sales', '')).username
        self.serializer.validated_data['buyer_id'] = user
        self.serializer.validated_data['sales_id'] = sale
        self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_200_OK, 'data': {'list_num': self.serializer.validated_data['num_list']}}
        return JsonResponse(result)

    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        orders = self.queryset.filter(num_list=pk)
        if orders:
            orders[0].status += 1
            result = {'code': status.HTTP_202_ACCEPTED}
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST}
        return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def destroy(self, request, pk=None):
        order = get_object_or_404(self.queryset, num_list=pk)
        if order:
            if order.buyer.username == request.user.username:
                order.delete()
                result = {'code': status.HTTP_202_ACCEPTED}
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'Who are you ?'}
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'Something must be wrong'}
        return Response(data=result)
