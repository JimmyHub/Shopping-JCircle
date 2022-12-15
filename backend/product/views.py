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

from Store.decorator import allmethods, trycatch, request_response
from Store.tool import get_json_data, get_serializer_data

from Store.authentication import TokenExAuthentication

key = 'a123456'


@allmethods(trycatch)
class ProductViewSet(GenericViewSet):
    queryset = ProductProfile.objects.all()
    serializer_class = ProductBaseSerializer
    authentication_classes = [TokenExAuthentication, ]

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ProductBaseSerializer
        else:
            return ProductSerializer

    def list(self, request, keyword=None, pattern=None, personal=None, record=None):
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
                    products = self.queryset.filter(sales=username).values()
            else:
                # 在一般用戶情況下瀏覽商品
                products = self.queryset.values()
            result = {'code': 200, 'data': list(products)}
            return JsonResponse(result)

        # 透過 pattern 判斷是否請求瀏覽紀錄
        elif pattern == 'record':
            list_key = record.split("&")
            no_key = 0
            list_record = []
            for i in list_key:
                if i == '0':
                    no_key += 1
                else:
                    products = self.queryset.filter(id=int(i)).values('id', 'pname', 'pphoto', 'pprice')
                    if products:
                        list_record.append(list(products)[0])

            if no_key == 3:
                result = {'code': 200, 'data': 'norecord'}
                return JsonResponse(result)
            else:
                result = {'code': 200, 'data': list(list_record)}
                return JsonResponse(result)

        # 透過 pattern 判斷是否查詢所有類別
        elif pattern == 'allkind':
            list_kind = self.queryset.values('pkind')
            result = {'code': 200, 'data': list(list_kind)}
            return JsonResponse(result)
        else:
            products = self.queryset.filter(id=keyword).values()
            if products:
                result = {'code': 200, 'data': list(products)[0]}
                return Response(data=result)
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST}
                return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['POST'])
    def create(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data, request)
        self.serializer.validated_data['sales_id'] = request.user.username
        new_product = self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_201_CREATED, 'pid': new_product.id}
        return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)
        get_serializer_data(self, data, request, partial=True)
        product = ProductProfile.objects.filter(id=pk)
        if product:
            product.update(**self.serializer.validated_data)
            result = {'code': status.HTTP_202_ACCEPTED}
            return Response(data=result)
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST}
            return Response(data=result)

    def destroy(self, request, pk=None):
        # 確認是否登入之後
        # 透過Keyword 找到商品 確認商品跟 登入者帳號是否相同
        product = get_object_or_404(ProductProfile, id=pk)
        if product.sales_id != request.user.username:
            raise SystemError('操作人員錯誤')
        # 確認訂單中是不是還有此商品
        order_products = OrderList.objects.filter(product_id=product.id).values('num_list', 'count')
        # 若現有訂單無此商品則可以刪除
        if order_products:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'This product is in some orders now',
                      'data': order_products}
            return Response(data=result)
        else:
            product.delete()
            result = {'code': status.HTTP_204_NO_CONTENT}
            return Response(data=result)


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
