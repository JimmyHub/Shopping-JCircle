import json
import jwt
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tools.tokens import login_check, auth_swagger_wrapper
from orderlist.models import OrderList

from .models import ProductProfile
from .serializers import ProductBaseSerializer, ProductSerializer
from rest_framework.viewsets import GenericViewSet
from django.db import transaction
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from drf_yasg import openapi

from Store.decorator import allmethods, trycatch, request_response
from Store.tool import get_json_data, get_serializer_data

from Store.authentication import TokenExAuthentication

key = 'a123456'

@allmethods(trycatch)
class ProductView(GenericAPIView):
    queryset = ProductProfile.objects.all()
    serializer_class = ProductBaseSerializer

    # @swagger_auto_schema(
    #     operation_summary='我是 GET 的摘要',
    #     operation_description='我是 GET 的說明',
    #     manual_parameters=[
    #        openapi.Parameter(
    #            name='keyword',
    #            in_=openapi.IN_PATH,
    #            type=openapi.TYPE_STRING
    #        ),
    #         openapi.Parameter(
    #             name='pattern',
    #             in_=openapi.IN_PATH,
    #             type=openapi.TYPE_STRING
    #         )
    #    ]
    # )
    def get(self, request,keyword=None,pattern=None,personal=None,record=None):
        # 透過 pattern 判斷是單獨查詢特定商品 還是整體商品
        if pattern == 'all':
            # 如果是請求整體商品資訊
            # 判斷瀏覽是在個人賣場內部(personal=1) 還是 一般用戶情況(personal=0)
            if personal == '1':
                # 判斷是由 哪個賣場老闆發起請求
                token = request.META.get('HTTP_AUTHORIZATION')
                if token:
                    try:
                        token_de = jwt.decode(token, key, algorithms=['HS256'])
                    except jwt.ExpiredSignatureError as e:
                        result = {'code': 401, 'error': 'please login one more time!'}
                        return JsonResponse(result)
                    # 或是解密出來 不正確也要中斷
                    except Exception as e:
                        result = {'code': 401, 'error': 'please login'}
                        return JsonResponse(result)
                    username = token_de['username']
                    # 賣場老闆發起請求 則是在賣場中瀏覽自己賣場的情況
                    products = ProductProfile.objects.filter(sales=username)
            else:

                # 在一般用戶情況下瀏覽商品
                products = ProductProfile.objects.all()
            product_list = []
            for i in products:
                data = {
                    'pid': i.id,
                    'pname': i.pname,
                    'pkind': i.pkind,
                    'pphoto': str(i.pphoto),
                    'pcontent': i.pcontent,
                    'pprice': i.pprice,
                    'sales': i.sales_id
                }
                product_list.append(data)
                # print(i._state.adding)
                # print(i._state.db)
                # print('----------')

            result = {'code': 200, 'data': product_list}
            return JsonResponse(result)

        # 透過 pattern 判斷是否請求瀏覽紀錄
        elif pattern == 'record':
            list_key = record.split("&")
            no_key = 0
            list_record = []
            for i in list_key:
                if i == '0':
                    no_key += 1
                    continue
                else:
                    products = ProductProfile.objects.filter(id=int(i))
                    if not products:
                        continue
                    data = {
                        'pid': products[0].id,
                        'pname': products[0].pname,
                        'pphoto': str(products[0].pphoto),
                        'pprice': products[0].pprice,
                    }
                    list_record.append(data)
            if no_key == 3:
                result = {'code': 200, 'data': 'norecord'}
                return JsonResponse(result)
            else:
                result = {'code': 200, 'data': list_record}
                return JsonResponse(result)

        # 透過 pattern 判斷是查詢特定類別 還是包含特定關鍵字商品
        elif pattern == 'search':
            # 如果Keyword 是空則返回無商品
            if not keyword:
                result = {'code': 200, 'data': 'NoProduct'}
                return JsonResponse(result)
            products = ProductProfile.objects.filter(pkind=keyword)
            # 若非特定類別,則是查詢包含特定關鍵字商品
            if not products:
                products = ProductProfile.objects.filter(pname__contains=keyword)
                # 若非包含特定關鍵字商品,則是查詢特定商品
                if not products:
                    # 判斷此時keyword 是不是數字 如果不是，就直接返回沒有此商品
                    if keyword.isdigit():
                        products = ProductProfile.objects.filter(id=keyword)
                        if not products:
                            result = {'code': 200, 'data': 'NoProduct'}
                            return JsonResponse(result)
                    else:
                        result = {'code': 200, 'data': 'NoProduct'}
                        return JsonResponse(result)
                    result = {'code': 200, 'data': {'pid': products[0].id,
                                                    'pname': products[0].pname,
                                                    'pkind': products[0].pkind,
                                                    'pphoto': str(products[0].pphoto),
                                                    'pcontent': products[0].pcontent,
                                                    'pprice': products[0].pprice,}}
                    return JsonResponse(result)
            # 若是包含特定類別商品 或是包含特定關鍵字的商品
            product_list = []
            for i in products:
                data = {
                    'pid': i.id,
                    'pname': i.pname,
                    'pkind': i.pkind,
                    'pphoto': str(i.pphoto),
                    'pcontent': i.pcontent,
                    'pprice': i.pprice,
                }
                product_list.append(data)
            result = {'code': 200, 'data': product_list}
            return JsonResponse(result)
        # 透過 pattern 判斷是否查詢所有類別
        elif pattern == 'allkind':
            products = ProductProfile.objects.all()
            list_kind = []
            for i in products:
                data = {
                    'pkind': i.pkind
                }
                list_kind.append(data)
            result = {'code': 200, 'data': list_kind}
            return JsonResponse(result)

        # pass
        # users = self.get_queryset()
        # serializer = self.serializer_class(users, many=True)
        # data = serializer.data
        # return JsonResponse(data, safe=False)

@allmethods(trycatch)
class ProductViewSet(GenericViewSet):
    queryset = ProductProfile.objects.all()
    serializer_class = ProductBaseSerializer
    authentication_classes = [TokenExAuthentication,]

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ProductBaseSerializer
        else:
            return ProductSerializer

    # @request_response(response_schema_dict=users_response_dict['POST'])
    def create(self, request):
        data = get_json_data(request.body)
        # data['sales_id'] = request.user
        get_serializer_data(self, data, request)
        self.serializer.validated_data['sales_id'] = request.user.username
        new_product = self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_201_CREATED, 'pid':new_product.id}
        return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)
        get_serializer_data(self, data, request, partial=True)
        product = get_object_or_404(ProductProfile,id=pk)
        self.serializer.validated_data['user'] = request.user
        self.serializer.update(instance=product, data=self.serializer.validated_data)
        result = {'code': status.HTTP_202_ACCEPTED}
        return Response(data=result)

    def destroy(self, request, pk=None):
        # 確認是否登入之後
        # 透過Keyword 找到商品 確認商品跟 登入者帳號是否相同
        product = get_object_or_404(ProductProfile,id=pk)
        # 確認訂單中是不是還有此商品
        if product.sales_id != request.user.username:
            raise SystemError('操作人員錯誤')
        order_products = OrderList.objects.filter(product_id=product.id).values('num_list','count')
        # 若現有訂單無此商品則可以刪除
        if order_products:
            # op_list = order_products.values('num_list','count')
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'This product is in some orders now', 'data': order_products}
            return Response(data=result)
        else:
            product.delete()
            result = {'code': status.HTTP_204_NO_CONTENT}
            return Response(data=result)

class ProductUPView(GenericViewSet):
    queryset = ProductProfile.objects.all()
    serializer_class = ProductBaseSerializer

    @auth_swagger_wrapper('', '')
    @login_check('DELETE')
    def delete(self, request, keyword):
        # 確認是否登入之後
        # 透過Keyword 找到商品 確認商品跟 登入者帳號是否相同
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result = {'code': 410, 'error': 'This product does not exist'}
            return JsonResponse(result)
        # 確認訂單中是不是還有此商品
        order_products = OrderList.objects.filter(product_id=keyword)
        # 若現有訂單無此商品則可以刪除
        if not order_products:
            # 檢視刪除者跟上傳者是否是同一個人
            sales_name = products[0].sales_id
            username = 'jimmy88'
            # username = request.user.name
            if sales_name != username:
                result = {'code': 401, 'error': 'Who are you ?'}
                return JsonResponse(result)
            else:
                products[0].delete()
                result = {'code': 200, 'data': username}
                return JsonResponse(result)
        else:
            op_list = []
            for op in order_products:
                print(op.num_list.num_list)
                dict_op = {
                    'list_num': 'jCircle' + str(op.num_list.num_list),
                    'count': op.count,
                }
                op_list.append(dict_op)
            result = {'code': 400, 'error': 'This product is in some orders now', 'data': op_list}
            return JsonResponse(result)
        # pass
        # product = self.get_object(id)
        # product.delete()
        # return JsonResponse(status=status.HTTP_204_NO_CONTENT)


class ProductPhoto(GenericAPIView):
    queryset = ProductProfile.objects.all()
    serializer_class = ProductBaseSerializer

    @auth_swagger_wrapper('Product_Photo', '')
    @login_check('POST')
    def post(self, request, keyword):
        if request.method != 'POST':
            result = {'code': 400, 'error': 'This is not post request'}
            return JsonResponse(result)
        if not keyword:
            result = {'code': 400, 'error': 'please give me keyword'}
            return JsonResponse(result)
        photo = request.FILES.get('photo')
        if not photo:
            result = {'code': 400, 'error': 'please give me photo'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result = {'code': 410, 'error': 'This product does not exist'}
            return JsonResponse(result)
        product = products[0]
        print('有porduct')
        try:
            product.pphoto = photo
        except:
            result = {'code': 500, 'error': 'the system is busy'}
            return JsonResponse(result)
        product.save()
        result = {'code': 200}
        return JsonResponse(result)
