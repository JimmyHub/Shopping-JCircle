from django.http import JsonResponse
from tools.tokens import login_check
from user.models import UserProfile
from .models import OrdersFiles
from orderlist.models import OrderList
from tools.Ecpay import *
import json
# Create your views here.
@login_check('GET','POST','PUT','DELETE')
def orders(request,keyword=None,mode=None):
    #訂單瀏覽
    if request.method=='GET':
        #獲取訂單資料(不包含商品資料)
        if keyword == None:
            result={'code':400,'error':'please give me keyword of list'}
            return JsonResponse(result)
        #keyword = 0 > 訂單總攬獲取
        if keyword == '0':
            #賣場總覽獲取
            if mode == '1':
                list_g=OrdersFiles.objects.filter(sales_id=request.user.name)
            #個人總覽獲取
            elif mode =='0':
                list_g=OrdersFiles.objects.filter(buyer_id=request.user.name)
            if list_g:
                list_orders=[]
                for i in list_g:
                    products_inOder = OrderList.objects.filter(num_list_id=i.num_list)
                    if not products_inOder:
                        result={'code':410,'error':'Something must be wrong'}
                        return JsonResponse(result)
                    item=(products_inOder[0].product.pname,products_inOder[0].count)
                    data={
                        'num_list':'jCircle'+str(i.num_list),
                        'num_time':i.num_time,
                        'status':i.status,
                        'status_time':i.status_time,
                        'money_total':i.money_total,
                        'products':item
                    }
                    list_orders.append(data)
                result={'code':200,'data':list_orders}
                return JsonResponse(result)
            else:
                result = {'code':200, 'data':'noorders'}
                return JsonResponse(result)
        else:
            #訂單資料詳細顯示
            list_g= OrdersFiles.objects.filter(num_list=keyword)
            if not list_g:
                result={'code':410,'error':'This list does not exist'}
                return JsonResponse(result)
            data={
                'num_list':'jCircle'+str(list_g[0].num_list),
                'num_time':list_g[0].num_time,
                'status':list_g[0].status,
                'status_time':list_g[0].status_time,
                'gname':list_g[0].gname,
                'address':list_g[0].address,
                'phone':list_g[0].phone,
                'payway':list_g[0].payway,
                'content':list_g[0].content,
                'bonus':list_g[0].bonus,
                'shipping':list_g[0].shipping,
                'money_total':list_g[0].money_total,
                'item':'jCircle商品一組',
                'CheckMacValue': ecpay_jc(list_g[0].num_list)
            }
            result={'code':200,'data':data}
            return JsonResponse(result)
    #訂單創立   
    elif request.method=='POST':
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        #訂單編號
        list_num = json_obj.get('list_num')
        if not list_num:
            result={'code':400,'error':'please give number of list'}
            return JsonResponse(result)
        #訂單時間
        list_time = json_obj.get('list_time')
        if not list_time:
            result={'code':400,'error':'please give time of list'}
            return JsonResponse(result)
        #訂單狀態
        status = json_obj.get('status')
        if not status:
            result={'code':400,'error':'please give status'}
            return JsonResponse(result)
        #收貨人姓名
        gname = json_obj.get('gname')
        if not gname:
            result={'code':400,'error':'please give gname'}
            return JsonResponse(result)
        #地址
        address = json_obj.get('address')
        if not address:
            result={'code':400,'error':'please give address'}
            return JsonResponse(result)
        #手機
        phone = json_obj.get('phone')
        if len(phone) != 10 :
            result={'code':400,'error':'please give real phone number'}
            return JsonResponse(result)

        #付款方式
        payway = json_obj.get('payway')
        if not payway:
            result={'code':400,'error':'please give payway'}
            return JsonResponse(result)
        #備註
        content = json_obj.get('content')
        if not content:
            result={'code':400,'error':'please give content'}
            return JsonResponse(result)
        #優惠
        bonus = json_obj.get('bonus')
        if int(bonus) < 0:
            result={'code':400,'error':'please give bonus'}
            return JsonResponse(result) 
        #運費
        shipping = json_obj.get('shipping')
        if not shipping:
            result={'code':400,'error':'please give shipping'}
            return JsonResponse(result)                     
        #總金額
        money_total = json_obj.get('money_total')
        if not money_total:
            result={'code':400,'error':'please give money_total'}
            return JsonResponse(result)
        #購買人
        buyer = json_obj.get('buyer')
        if not buyer:
            result={'code':400,'error':'please give buyer'}
            return JsonResponse(result)
        #販售人
        sales = json_obj.get('sales')
        if not buyer:
            result={'code':400,'error':'please give sales'}
            return JsonResponse(result)            
        user=UserProfile.objects.filter(name=buyer)
        if not user:
            result={'code':410,'error':'This user does not exist'}
            return JsonResponse(result)
        sale=UserProfile.objects.filter(name=sales)
        if not sale:
            result={'code':410,'error':'This sale does not exist'}
            return JsonResponse(result)
        try:
            OrdersFiles.objects.create(
                num_list=list_num,
                num_time=list_time, 
                status=int(status),
                gname=gname,
                address=address,
                phone=phone,
                payway=int(payway),
                content=content,
                bonus=int(bonus),
                shipping=int(shipping),
                money_total=int(money_total),
                buyer=user[0],
                sales=sale[0]
            )
        except:
            result={'code':500,'error':'System is busy'}
            return JsonResponse(result)
        result={'code':200,'data':{'list_num':list_num}}
        return JsonResponse(result) 
    #訂單更改
    elif request.method=='PUT':
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        keyword =json_obj.get('keyword')
        if not keyword:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)                
        orders = OrdersFiles.objects.filter(num_list=keyword)
        if not orders:
            result={'code':410,'error':'Something must be wrong'}
            return JsonResponse(result)
        try:
            #將訂單狀態往下修改一個
            orders[0].status+=1
        except:
            result={'code':500,'error':'System is busy'}
            return JsonResponse(result)
        orders[0].save()
        result={'code':200,'data':'ok'}
        return JsonResponse(result)
    #訂單刪除
    elif request.method=='DELETE':
        if keyword == None:
            result={'code':400,'error':'please give me keyword of list'}
            return JsonResponse(result)
        orders = OrdersFiles.objects.filter(num_list=keyword)
        if not orders:
            result={'code':410,'error':'Something must be wrong'}
            return JsonResponse(result)
        if request.user.name != orders[0].buyer.name:
            result={'code':400,'error':'Who are you ?'}
            return JsonResponse(result)
        else:
            orders[0].delete()
        result={'code':200}
        return JsonResponse(result)


	
