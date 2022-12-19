import jwt

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Store.decorator import allmethods, trycatch, request_response
from Store.tool import get_json_data, get_serializer_data
from Store.authentication import TokenExAuthentication
from tools.tokens import login_check, auth_swagger_wrapper
from orderlist.models import OrderList

from .models import ProductProfile
from .serializers import ProductBaseSerializer, ProductSerializer



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
                # 賣場老闆發起請求 則是在賣場中瀏覽自己賣場的情況
                products = self.queryset.filter(sales=request.user.username).values()
            else:
                # 在一般用戶情況下瀏覽商品
                products = self.queryset.values()
            result = {'code': 200, 'data': list(products)}

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
            else:
                result = {'code': 200, 'data': list(list_record)}

        # 透過 pattern 判斷是否查詢所有類別
        elif pattern == 'allkind':
            list_kind = self.queryset.values('pkind')
            result = {'code': 200, 'data': list(list_kind)}
        else:
            products = self.queryset.filter(id=keyword).values()
            if products:
                result = {'code': 200, 'data': list(products)[0]}
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST}
        return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['POST'])
    def create(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data)
        self.serializer.validated_data['sales_id'] = request.user.username
        new_product = self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_201_CREATED, 'pid': new_product.id}
        return Response(data=result)

    # @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)
        get_serializer_data(self, data, partial=True)
        product = self.queryset.filter(id=pk)
        if product:
            product.update(**self.serializer.validated_data)
            result = {'code': status.HTTP_202_ACCEPTED}
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
            return Response(data=result)
        if not keyword:
            result = {'code': 400, 'error': 'please give me keyword'}
            return Response(data=result)
        photo = request.FILES.get('photo')
        if not photo:
            result = {'code': 400, 'error': 'please give me photo'}
            return Response(data=result)
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result = {'code': 410, 'error': 'This product does not exist'}
            return Response(data=result)
        product = products[0]
        try:
            product.pphoto = photo
        except:
            result = {'code': 500, 'error': 'the system is busy'}
            return Response(data=result)
        product.save()
        result = {'code': 200}
        return Response(data=result)
