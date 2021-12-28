#帳號密碼
def make_token(username,expire=3600*24):
    #生成token 返回給前端
    now=time.time()
    limit_time=now+expire
    payload={'username':username,'exp':limit_time}
    return jwt.encode(payload,key,algorithm='HS256')


m=hashlib.md5()
m.update(password.encode())
p=m.hexdigest()
try:
    #避免註冊時網頁出錯 造成註冊不完全
    UserProfile.objects.create(name=name,
                               password=p,
                               phone=phone,
                               email=email)
except:
    result={'code':500,'error':'Server is busy'}
    return JsonResponse(result)
token = make_token(name)
result = {'code': 200,'data':{'username': name,'token': token}}
return JsonResponse(result)

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
#金流串接 模擬繳費
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
                check_origin += list_item[i]+'='+str(get)+("&HashIV=%s"%HashIV)
            else:
                check_origin += list_item[i]+'='+str(get)+"&"
        CheckMacValue_o=check_encode(check_origin)
        CheckMac_get=request.POST.get('CheckMacValue',None)
        RtnCode=request.POST.get('RtnCode',0)
        #務必判斷交易狀態[RtnCode]是否為1，
        #若非1 時請勿對該筆交易做出貨動作，並取得交易訊息[RtnMsg] 記錄失敗原因。
        if RtnCode == "1" :
            print('交易成功')
            if CheckMac_get == CheckMacValue_o:
                orders=OrdersFiles.objects.filter(id=list_id)
                if not orders:
                    result={'code':400,'error':'please give me data'}
                    return JsonResponse(result)
                try:
                    orders[0].status +=1
                    orders[0].save() 
                except:
                    result={'code':500,'error':'System is busy'}
                    return JsonResponse(result) 
                return HttpResponse('1|OK')
        else:
            result={'code':400,'error':'the deal does not success'}
            return JsonResponse(result)