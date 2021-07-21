from django.http import JsonResponse
from tools.tokens import login_check
import json
from product.models import ProductProfile
from .models import ShoppingList
# Create your views here.    count_g=None
key='a123456'
@login_check('GET','POST','PUT','DELETE')
def shoppingcarts(request,keyword=None):
    if request.method =='GET':
        user = request.user
        if not user:
            result={'code':401,'error':'please login'}
            return JsonResponse(result)
        carts=ShoppingList.objects.filter(user=user.name)
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
                'price':i.price,
                'count':i.count,
                'sales':i.product.sales.name
            }
            data.append(dic_cart)
        result={'code':200,'data':data}
        return JsonResponse(result)

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
        price = int(json_obj.get('price'))
        if not price:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        count = int(json_obj.get('count'))
        if not count:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        try:
            ShoppingList.objects.create(price=price,
                                        count=count,
                                        product=products[0],
                                        user=user)
        except:
            result={'code':500,'error':'System is busy'}
            return JsonResponse(result)
        result={'code':200}
        return JsonResponse(result)
    
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
        carts[0].save()
        result={'code':200}
        return JsonResponse(result)

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
