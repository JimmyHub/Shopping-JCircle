from order.models import OrdersFiles
from orderlist.models import OrderList
from django.http import  JsonResponse,HttpResponse
import hashlib ,requests,time, math ,json
from django.utils.http import urlquote



""" 金流驗證相關 模塊"""

MerchantID= "2000132"
PaymentType="aio"
TradeDesc="JCshoppingmall"
EncryptType=1
#綠界API
url="https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"
#KEY要加頭
HashKey="5294y06JbISpM5x9"
#IV加尾吧
HashIV="v77hoKGq4kWxNNIS"
ClientBackURL="http://www.jcircle.ml/#/orders"
OrderResultURL="http://www.jcircle.ml/#/orders"
#CheckMacValue 驗證碼生成
def check_encode(origin):
    # 1.urlencode
    a = urlquote(origin)
    # 2.替換成.net code
    str02 = ''

    for i in a:
        if i == '/':
            str02 += '%2f'
        else:
            str02 += i
    b = str02.replace('%20', '+')
    # 3.轉換成小寫
    c = b.lower()
    # 4.進行 SHA256緊湊
    m = hashlib.sha256()
    m.update(c.encode())
    d = m.hexdigest()
    # 5.轉成大寫
    e = d.upper()
    return e

#驗證碼生成  前置數據生成
def ecpay_jc(list_id):
    #透過order id 從現有OrdersFiles 數據庫 拿數據出來
    if not list_id:
        result={'code':400,'error':'please give me data'}
        return JsonResponse(result)
    orders= OrdersFiles.objects.filter(id=list_id)
    if not orders:
        result={'code':410,'error':'This list does not exist'}
        return JsonResponse(result)
    if orders[0].payway == 1:
        ChoosePayment="Credit"
    elif orders[0].payway == 2:
        ChoosePayment="BARCODE"
    MerchantTradeNo ="jCircle"+str(orders[0].num_list)
    MerchantTradeDate=orders[0].num_time[0:10]+' '+orders[0].num_time[11:19]
    TotalAmount=orders[0].money_total 
    ItemName='jCircle商品一組'
    ReturnURL="http://www.jcircle.ml/api/v1/CheckMacValue/"+str(list_id)
    check_origin="HashKey=%s&ChoosePayment=%s&ClientBackURL=%s&EncryptType=%d&ItemName=" \
                 "%s&MerchantID=%s&MerchantTradeDate=%s&MerchantTradeNo=%s&OrderResultURL=%s&PaymentType=%s&ReturnURL=" \
                 "%s&TotalAmount=%d&TradeDesc=%s&HashIV=%s"%(HashKey,ChoosePayment,ClientBackURL,EncryptType,ItemName,MerchantID,MerchantTradeDate,MerchantTradeNo,OrderResultURL,PaymentType,ReturnURL,TotalAmount,TradeDesc,HashIV)
    CheckMacValue = check_encode(check_origin)
    return CheckMacValue


#訂單繳費成立回調
def CheckMacValue(request,list_id):
    if request.method =="POST":
        if not list_id:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        list_item=['MerchantID','MerchantTradeNo','PaymentDate','PaymentType','PaymentTypeChargeFee','RtnCode','RtnMsg','SimulatePaid','StoreID','TradeAmt','TradeDate','TradeNo']
        check_origin='HashKey=%s&CustomField1=&CustomField2=&CustomField3=&CustomField4=&'%HashKey
        for i in range(len(list_item)):
            get = request.POST.get(list_item[i],'')
            if i == len(list_item)-1:
                #check_origin += list_item[i]+'='+str(get)
                check_origin += list_item[i]+'='+str(get)+("&HashIV=%s"%HashIV)
            else:
                check_origin += list_item[i]+'='+str(get)+"&"
        #print(check_encode(check_origin))
        CheckMacValue_o=check_encode(check_origin)
        CheckMac_get=request.POST.get('CheckMacValue',None)
        #print(CheckMac_get)
        RtnCode=request.POST.get('RtnCode',0)
        #務必判斷交易狀態[RtnCode]是否為1，若非1 時請勿對該筆交易做出貨動作，並取得交易訊息[RtnMsg] 記錄失敗原因。
        if RtnCode == "1" :
            print('交易成功')
            if CheckMac_get == CheckMacValue_o:
                orders=OrdersFiles.objects.filter(id=list_id)
                if not orders:
                    result={'code':400,'error':'please give me data'}
                    return JsonResponse(result)
                try:
                    orders[0].status =1
                    orders[0].save() 
                except:
                    result={'code':500,'error':'System is busy'}
                    return JsonResponse(result) 
                return HttpResponse('1|OK')
        else:
            result={'code':400,'error':'the deal does not success'}
            return JsonResponse(result)
    else:
        result={'code':400,'error':'please use post method'}
        return JsonResponse(result)  

#訂單創建成立查詢
def orderCheck(request,keyword):
    if not keyword:
        result={'code':400,'error':'please give me list number'}
        return JsonResponse(result)
    orders = OrdersFiles.objects.filter(id=keyword)
    if not orders:
        result={'code':410,'error':'This order don`t exist'}
        return JsonResponse(result)
    MerchantTradeNo = "jCircle"+str(orders[0].num_list)
    time_now=math.floor(time.time())
    check_origin="HashKey=%s&MerchantID=%s&MerchantTradeNo=%s&TimeStamp=%d&HashIV=%s"%(HashKey,MerchantID,MerchantTradeNo,time_now,HashIV)
    CheckMacValue = check_encode(check_origin)
    result={'code':200,'data':{'check':CheckMacValue,'time':time_now}}
    return JsonResponse(result)