import json

import jwt
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from tools.tokens import login_check
from .models import ProductProfile
from orderlist.models import OrderList
key='a123456'

@login_check('POST','PUT','DELETE')
def products(request,keyword=None,personal=None,key1=None,key2=None,key3=None):
    if request.method == 'GET':
        #判斷是單獨查詢特定商品 還是整體商品
        if keyword == '0':
            #如果是請求整體商品資訊 
            #判斷瀏覽是在個人賣場內部(personal_market=1) 還是 一般情況(personal_market=0)
            if personal ==  '1' :
            #判斷是由 哪個賣場老闆發起請求
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
                    #賣場老闆發起請求 則是在賣場中瀏覽自己賣場的情況
                    products=ProductProfile.objects.filter(sales=username)
            else:
                #在一般情況下瀏覽商品的情況
                products = ProductProfile.objects.all()
            product_list = []
            for i in products:
                data = {
                    'pid':i.id,
                    'pname': i.pname,
                    'pkind': i.pkind,
                    'pphoto': str(i.pphoto),
                    'pcontent': i.pcontent,
                    'pprice': i.pprice,
                    'pway': i.pway,
                }
                product_list.append(data)
            result = {'code': 200, 'data': product_list}
            return JsonResponse(result)
        else:
            #特定查詢情況
            if keyword =='record':
                #判斷是否請求瀏覽紀錄
                key1_g = key1
                key2_g = key2
                key3_g = key3
                if key1_g ==0:
                    if key2_g ==0:
                        if key3_g ==0:
                            result={'code':200,'data':'norecord'}
                            return JsonResponse(result)
                record_key=[key3,key2,key1]
                list_record=[]
                for i in record_key:
                   products=ProductProfile.objects.filter(id=i)
                   #如果沒有products 就跳過
                   if not products:
                       continue
                   data={
                        'pid':products[0].id,
                        'pname': products[0].pname,
                        'pphoto': str(products[0].pphoto),
                        'pprice': products[0].pprice,
                   }
                   list_record.append(data)
                result={'code':200,'data':list_record}
                return JsonResponse(result)
            else:
                #判斷是查詢特定類別 還是包含特定關鍵字商品
                products=ProductProfile.objects.filter(pkind=keyword)
                if not products:
                    #若非特定類別,則是查詢包含特定關鍵字商品 
                    products=ProductProfile.objects.filter(pname__contains=keyword)
                    #若非包含特定關鍵字商品,則是查詢特定商品
                    if not products:
                        #判斷此時keyword 是不是數字 如果不是，就直接返回沒有此商品
                        if keyword.isdigit():
                            products = ProductProfile.objects.filter(id=keyword)
                            if not products:
                                result = {'code': 200, 'data': 'NoProduct'}
                                return JsonResponse(result)
                        else:
                            result = {'code': 200, 'data': 'NoProduct'}
                            return JsonResponse(result)
                        result={'code':200,'data':{'pid':products[0].id,
                                               'pname': products[0].pname,
                                               'pkind': products[0].pkind,
                                              'pphoto': str(products[0].pphoto),
                                            'pcontent': products[0].pcontent,
                                              'pprice': products[0].pprice,
                                                'pway': products[0].pway,}}
                        return JsonResponse(result)
                product_list = []
                for i in products:
                    data = {
                        'pid':i.id,
                        'pname': i.pname,
                        'pkind': i.pkind,
                        'pphoto': str(i.pphoto),
                        'pcontent': i.pcontent,
                        'pprice': i.pprice,
                        'pway': i.pway,
                    }
                    product_list.append(data)
                result = {'code': 200, 'data': product_list}
                return JsonResponse(result)
    
    elif request.method =='POST':
        user=request.user
        if not user:
            result={'code':410,'error':'this user does not exist'}
            return JsonResponse(result)
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        pname = json_obj.get('pname')
        if not pname:
            result={'code':400,'error':'please give me product name'}
            return JsonResponse(result)
        pkind =json_obj.get('pkind')
        if not pkind:
            result={'code':400,'error':'please give me product kind'}
            return JsonResponse(result)
        pcontent=json_obj.get('pcontent')
        if not pcontent:
            result={'code':400,'error':'please give me product content'}
            return JsonResponse(result)
        pprice = json_obj.get('pprice')
        if not pprice:
            result={'code':400,'error':'please give me product price'}
            return JsonResponse(result)
        pway = json_obj.get('pway')
        if not pway:
            result={'code':400,'error':'please give me product pway'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(sales_id=user.name)
        for i in products:
            if i.pname == pname:
                result={'code':400,'error':'this product is existing'}
                return JsonResponse(result)
        try:
            # 避免上傳時網頁出錯 造成上傳不完全
            ProductProfile.objects.create(pname=pname,
                                          pkind=pkind,
                                          pcontent=pcontent,
                                          pprice=pprice,
                                          pway=int(pway),
                                          sales_id=user.name)
        except:
            result={'code':500,'error':'System is busy.'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(sales_id=user.name)
        id=0
        for i in products:
            if i.pname == pname:
                id = i.id
        result={'code':200,'pid':id}
        return JsonResponse(result)
    #商品修改
    elif request.method =='PUT':
        if not keyword:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result={'code':400,'error':'this product does not exist'}
            return JsonResponse(result)
        product=products[0]
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        pname = json_obj.get('pname')
        #如果沒有 沒有哪一種資料 就不用改哪一種
        if pname != '':
            products_check = ProductProfile.objects.filter(pname=pname)
            #確保修改商品名稱後 不會改成相同的商品
            if products_check:
                result={'code':400,'error':'This pname already exist'}
                return JsonResponse(result)
            product.pname = pname
        pkind = json_obj.get('pkind')
        if pkind !='':
            product.pkind= pkind
        pcontent=json_obj.get('pcontent')
        if pcontent !='':
            product.pcontent=pcontent
        pprice = json_obj.get('pprice')
        if pprice != '':
            product.pprice=int(pprice)
        pway = json_obj.get('pway')
        if pway != 0:
            product.pway=int(pway)
        product.save()
        result={'code':200,'data':{'pname':product.pname}}
        return JsonResponse(result)
    #商品刪除
    elif request.method =='DELETE':
        #確認是否登入之後
        #透過Keyword 找到商品 確認商品跟 登入者帳號是否相同 
        products = ProductProfile.objects.filter(id=keyword)
        if not products:
            result={'code':410,'error':'This product does not exist'}
            return JsonResponse(result)
        #確認訂單中是不是還有此商品
        order_products = OrderList.objects.filter(product_id=keyword)
        #若現有訂單無此商品則可以刪除
        if not order_products:
            #檢視刪除者跟上傳者是否是同一個人
            sales_name = products[0].sales_id
            username = request.user.name
            if sales_name != username:
                result={'code':401,'error':'Who are you ?'}
                return JsonResponse(result)
            else:
                products[0].delete()
                result={'code':200,'data':username}
                return JsonResponse(result)
        else:
            op_list=[]
            for op in order_products:
                print(op.num_list.num_list)
                dict_op ={
                       'list_num':'jCircle'+ str(op.num_list.num_list),
                       'count':op.count,
                }
                op_list.append(dict_op)
            result = {'code':400,'error':'This product is in some orders now','data':op_list}
            return JsonResponse(result)
            
@login_check('POST')
def products_photo(request,keyword):
    if request.method !='POST':
        result={'code':400,'error':'This is not post request'}
        return JsonResponse(result)
    if not keyword:
        result={'code':400,'error':'please give me keyword'}
        return JsonResponse(result)
    photo = request.FILES.get('photo')
    print('有photo')
    if not photo:
        result={'code':400,'error':'please give me photo'}
        return JsonResponse(result)
    products=ProductProfile.objects.filter(id=keyword)
    if not products:
        result = {'code': 410, 'error': 'This product does not exist'}
        return JsonResponse(result)
    product = products[0]
    print('有porduct')
    try:
        product.pphoto = photo
    except:
        result={'code':500,'error':'the system is busy'}
        return JsonResponse(result)
    product.save()
    result = {'code':200}
    return JsonResponse(result)