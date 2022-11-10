import json
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView

from tools.tokens import login_check

from .models import ShoppingList
from .serializers import ShopSerializer
from product.models import ProductProfile


class ShoppingView(GenericAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShopSerializer

    # 購物車瀏覽
    @login_check('GET')
    def get(self,request,keyword):
        user = request.user
        if not user:
            result = {'code': 401, 'error': 'please login'}
            return JsonResponse(result)
        carts = ShoppingList.objects.filter(user=user.username)
        if not carts:
            result = {'code': 410, 'error': 'This shoppingcart is empty'}
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
                # 'sales':i.product.sales.name
            }
            data.append(dic_cart)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)

    # 購物車加入
    @login_check('POST')
    def post(self,request, keyword):
        user = request.user
        if not user:
            result = {'code': 401, 'error': 'please login'}
            return JsonResponse(result)
        if not keyword:
            result = {'code': 400, 'error': 'please give me keyword'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result = {'code': 410, 'error': 'This product does not exist'}
            return JsonResponse(result)
        json_str = request.body
        if not json_str:
            result = {'code': 400, 'error': 'please give data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        count = int(json_obj.get('count'))
        if not count:
            result = {'code': 400, 'error': 'please give data'}
            return JsonResponse(result)
        # 判斷購物車內是否已經有此商品,有的話 將數量加上
        product_exsist = ShoppingList.objects.filter(product_id=keyword)
        if product_exsist:
            try:
                old_count = product_exsist[0].count
                product_exsist[0].count = old_count + count
            except:
                result = {'code': 500, 'error': 'System is busy'}
                return JsonResponse(result)
            product_exsist[0].save()
        # 若購物車內還沒有此商品就加入購物車
        else:
            try:
                ShoppingList.objects.create(
                    count=count,
                    product=products[0],
                    user=user)
            except:
                result = {'code': 500, 'error': 'System is busy'}
                return JsonResponse(result)
        result = {'code': 200}
        return JsonResponse(result)

    # 購物車修改
    @login_check('PUT')
    def put(self,request, keyword):
        user = request.user
        if not user:
            result = {'code': 401, 'error': 'please login'}
            return JsonResponse(result)
        if not keyword:
            result = {'code': 400, 'error': 'please give me keyword'}
            return JsonResponse(result)
        json_str = request.body
        if not json_str:
            result = {'code': 400, 'error': 'please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        count_g = json_obj.get('count')
        carts = ShoppingList.objects.filter(id=keyword)
        if not carts:
            result = {'code': 410, 'error': 'This item does not exist'}
            return JsonResponse(result)
        try:
            carts[0].count = int(count_g)
        except:
            result = {'code': 500, 'error': 'System is busy!'}
            return JsonResponse(result)

        carts[0].save()
        result = {'code': 200}
        return JsonResponse(result)

    @login_check('DELETE')
    def delete(self,request, keyword):
        # 購物車刪除
        user = request.user
        if not user:
            result = {'code': 401, 'error': 'please login'}
            return JsonResponse(result)
        if not keyword:
            result = {'code': 400, 'error': 'please give me keyword'}
            return JsonResponse(result)
        carts = ShoppingList.objects.filter(id=keyword)
        if not carts:
            result = {'code': 410, 'error': 'This item does not exist'}
            return JsonResponse(result)
        carts[0].delete()
        result = {'code': 200}
        return JsonResponse(result)


@login_check('GET','POST','PUT','DELETE')
def shoppingcarts(request,keyword=None):
    #購物車瀏覽
    if request.method =='GET':
        user = request.user
        if not user:
            result={'code':401,'error':'please login'}
            return JsonResponse(result)
        carts=ShoppingList.objects.filter(user=user.username)
        if not carts:
            result={'code':410,'error':'This shoppingcart is empty'}
            return JsonResponse(result)
        data=[]
        for i in carts:
            dic_cart={
                'list_id':i.id,
                'pname':i.product.pname,
                'pid':i.product.id,
                'pkind':i.product.pkind,
                'pphoto':str(i.product.pphoto),
                'price':i.product.pprice,
                'count':i.count,
                #'sales':i.product.sales.name
            }
            data.append(dic_cart)
        result={'code':200,'data':data}
        return JsonResponse(result)
    #購物車加入
    elif request.method =='POST':
        user = request.user
        if not user:
            result={'code':401,'error':'please login'}
            return JsonResponse(result)
        if not keyword:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result={'code':410,'error':'This product does not exist'}
            return JsonResponse(result)
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        count = int(json_obj.get('count'))
        if not count:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        #判斷購物車內是否已經有此商品,有的話 將數量加上
        product_exsist = ShoppingList.objects.filter(product_id=keyword)
        if product_exsist:
            try:
                old_count = product_exsist[0].count
                product_exsist[0].count = old_count + count
            except:
                result={'code':500,'error':'System is busy'}
                return JsonResponse(result)
            product_exsist[0].save()
        #若購物車內還沒有此商品就加入購物車
        else:
            try:
                ShoppingList.objects.create(
                                            count=count,
                                            product=products[0],
                                            user=user)
            except:
                result={'code':500,'error':'System is busy'}
                return JsonResponse(result)
        result={'code':200}
        return JsonResponse(result)
    #購物車修改
    elif request.method =='PUT':
        user = request.user
        if not user:
            result={'code':401,'error':'please login'}
            return JsonResponse(result)
        if not keyword:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        count_g=json_obj.get('count')
        carts = ShoppingList.objects.filter(id=keyword)
        if not carts:
            result={'code':410,'error':'This item does not exist'}
            return JsonResponse(result)
        try:
            carts[0].count= int(count_g)
        except:
            result={'code':500,'error':'System is busy!'}
            return JsonResponse(result)

        carts[0].save()
        result={'code':200}
        return JsonResponse(result)
    #購物車刪除
    elif request.method =='DELETE':
        user = request.user
        if not user:
            result={'code':401,'error':'please login'}
            return JsonResponse(result)
        if not keyword:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        carts = ShoppingList.objects.filter(id=keyword)
        if not carts:
            result={'code':410,'error':'This item does not exist'}
            return JsonResponse(result)
        carts[0].delete()
        result={'code':200}
        return JsonResponse(result)
    else:
        result={'code':500,'error':'You use the wrong request'}
        return JsonResponse(result)
