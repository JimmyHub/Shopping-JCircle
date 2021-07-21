from django.http import JsonResponse,HttpResponse
from tools.tokens import login_check
from product.models import ProductProfile
from user.models import UserProfile
from order.models import OrdersFiles
from shoppingcart.models import ShoppingList
from .models import OrderList
from message.models import MessageRecord
from django.shortcuts import render
from tools.Ecpay import *
import json


# Create your views here.


@login_check('GET','POST','DELETE')
def orderlists(request,keyword=None,mode=None):
    if request.method=='GET':
        #訂單商品資料獲取
        if keyword == None:
            result={'code':200,'data':'noorders'}
            return JsonResponse(result)
        if mode == None:
            result={'code':400,'error':'please give me mode'}
            return JsonResponse(result)
        products=OrderList.objects.filter(num_list_id=keyword)
        if not products:
            result={'code':410,'error':'This list does not exist'}
            return JsonResponse(result)
        list_products=[]
        #訂單商品資料總覽 直接寫在orders view裡面 
        #mode =1 > 詳細訂單商品資料    
        for i in products:
            #賣場詳細訂單商品顯示
            if mode == '1':
                if i.sales.name == request.user.name:
                    dic_per_s={
                        'pname':i.product.pname,
                        'id':i.product.id,
                        'photo':str(i.product.pphoto),
                        'price':i.product.pprice,
                        'count':i.count,
                    }
                    list_products.append(dic_per_s)
            elif mode == '0':
                if i.num_list.buyer.name == request.user.name:
                #個人詳細訂單商品顯示
                    dic_per={
                        'pname':i.product.pname,
                        'id':i.product.id,
                        'photo':str(i.product.pphoto),
                        'price':i.product.pprice,
                        'count':i.count,
                    }
                    list_products.append(dic_per)
        result={'code': 200 ,'data': list_products }
        return JsonResponse(result)

    elif request.method=='POST':
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        #商品數量
        counts = json_obj.get('counts')
        if not counts:
            result={'code':400,'error':'please give counts'}
            return JsonResponse(result)
        #商品id
        products = json_obj.get('products')
        if not products:
            result={'code':400,'error':'please give products'}
            return JsonResponse(result)
        #訂單編號
        num_list = json_obj.get('num_list')
        if not num_list:
            result={'code':400,'error':'please give number of list'}
            return JsonResponse(result)
        list_p = OrdersFiles.objects.filter(num_list=num_list)
        if not list_p:
            result={'code':410,'error':'This list does not exist'}
            return JsonResponse(result)
         
        #商品販售人id
        sales = json_obj.get('sales')
        if not sales:
            result={'code':400,'error':'please give sales'}
            return JsonResponse(result) 
        #購物車商品id
        list_id = json_obj.get('list_id')
        if not list_id:
            result={'code':400,'error':'please give list_id'}
            return JsonResponse(result)
        try:
            for i in range(len(counts)):
                OrderList.objects.create(count=counts[i],
                                         product_id=products[i],
                                         num_list_id=list_p[0].id,
                                         sales_id=sales[i])
            for j in list_id:
                shoppingcart=ShoppingList.objects.filter(id=j)
                shoppingcart.delete()
        except:
            result={'code':500,'error':'System is busy'}
            return JsonResponse(result)
        result={'code':200,'data':list_p[0].id}
        return JsonResponse(result)

    elif request.method=='DELETE':
        if keyword == None:
            result={'code':400,'error':'please give me keyword of list'}
            return JsonResponse(result)
        if mode == None:
            result={'code':400,'error':'please give me mode'}
            return JsonResponse(result)
        products=OrderList.objects.filter(num_list_id=keyword)
        if not products:
            result={'code':410,'error':'This list does not exist'}
            return JsonResponse(result)
        for i in products:
            if request.user.name != i.num_list.buyer.name:
                result={'code':400,'error':'you can not do this!'}
                return JsonResponse(result)
            else:
                #mode = 0 表示是在結帳時退回上一頁 刪除清單 要加回購物車
                if mode == '0':
                    try:
                        ShoppingList.objects.create(price=i.product.pprice,
                                                    count=i.count,
                                                    product_id=i.product.id,
                                                    user_id=i.num_list.buyer.name)
                    except:
                        result={'code':500,'error':'System is busy'}
                        return JsonResponse(result)
                #mode = 1 表示是在我的訂單中刪除訂單 留言板 跟清單資料要先刪除 
                elif mode == '1':
                    msgs= MessageRecord.objects.filter(num_list_id=keyword)
                    if not msgs:
                        continue
                    else:
                        for m in msgs:
                            m.delete()
                i.delete()
        result={'code':200}
        return JsonResponse(result)




