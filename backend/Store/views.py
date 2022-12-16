import hashlib

from django.http import JsonResponse, HttpResponse
from rest_framework.generics import GenericAPIView
import jwt
from rest_framework.viewsets import GenericViewSet

from user.models import UserProfile
from user.serializers import UserSerializer
from tools.tokens import auth_swagger_wrapper

from order.models import OrdersFiles
from orderlist.models import OrderList
from django.http import JsonResponse, HttpResponse

IP = 'http://localhost'
PORT = 8080
key = 'a123456'
# 綠界API
url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"


class IndexView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @auth_swagger_wrapper('', '')
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == "null":
            result = {'code': 200, 'data': 'nouser'}
            return JsonResponse(result)
        else:
            try:
                token_de = jwt.decode(token, key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError as e:
                result = {'code': 401, 'error': 'please login one more time!'}
                return JsonResponse(result)
            username_de = token_de['username']
            auser = UserProfile.objects.filter(username=username_de)
            if not auser:
                result = {'code': 410, 'error': 'This user do not exist !'}
                return JsonResponse(result)
            if auser[0].username:
                username = auser[0].username
                avatar = str(auser[0].avatar)
                limit = auser[0].limit
                result = {'code': 200, 'data': {"username": username,
                                                "avatar": avatar,
                                                "limit": limit}}
                return JsonResponse(result)
            else:
                result = {'code': 410, 'error': 'This user do not exist !'}
                return JsonResponse(result)


class EcpayTrade:
    def __init__(self):
        self.dict = {
            # KEY要加頭
            "HashKey": "5294y06JbISpM5x9",
            "ChoosePayment": "",
            "ClientBackURL": f"{IP}:{PORT}/#/orders",
            "EncryptType": 1,
            "ItemName": "",
            "MerchantID": "2000132",
            "MerchantTradeDate": "",
            "MerchantTradeNo": "",
            "OrderResultURL": f"{IP}:{PORT}/#/orders",
            "PaymentType": "aio",
            "ReturnURL": "",
            "TotalAmount": 0,
            "TradeDesc": "JCshoppingmall",
            # IV加尾吧
            "HashIV": "v77hoKGq4kWxNNIS"}

    # CheckMacValue 驗證碼生成
    def check_encode(self, origin):
        # 1.urlencode
        origin_encode = urlquote(origin)
        # 2.替換成.net code
        origin_tmp = ''
        for i in origin_encode:
            if i == '/':
                origin_tmp += '%2f'
            else:
                origin_tmp += i
        origin_replace = origin_tmp.replace('%20', '+')
        # 3.轉換成小寫
        origin_lower = origin_replace.lower()
        # 4.進行 SHA256緊湊
        m = hashlib.sha256()
        m.update(origin_lower.encode())
        origin_hex = m.hexdigest()
        # 5.轉成大寫
        origin_final = origin_hex.upper()
        return origin_final

    # 驗證碼生成  前置數據生成
    def ecpay_jc(self, list_num):
        # 透過order id 從現有OrdersFiles 數據庫 拿數據出來
        orders = OrdersFiles.objects.filter(num_list=list_num)
        if not orders:
            result = {'code': 410, 'error': 'This list does not exist'}
            return JsonResponse(result)
        if orders[0].payway == 1:
            ChoosePayment = "Credit"
        elif orders[0].payway == 2:
            ChoosePayment = "BARCODE"
        # 透過API獲得參數數值後，根據參數查找資料庫的數據，直接用資料庫內查到的值作替代
        list_num_db = orders[0].num_list
        self.dict["MerchantTradeNo"] = "jCircle" + str(list_num_db)
        self.dict["MerchantTradeDate"] = orders[0].num_time[0:10] + ' ' + orders[0].num_time[11:19]
        self.dict["TotalAmount"] = orders[0].money_total
        self.dict["ItemName"] = 'jCircle商品一組'
        self.dict["ReturnURL"] = "http://www.jcircle.ml/api/v1/CheckMacValue/" + str(list_num_db)
        check_list = [f'{k}={v}' for k, v in self.dict.items()]
        check_origin = '&'.join(check_list)
        CheckMacValue = self.check_encode(check_origin)
        return CheckMacValue

    # 訂單繳費成立回調
    def CheckMacValue(self,request, list_num):
        if request.method == "POST":
            if not list_num:
                result = {'code': 400, 'error': 'please give me list_num'}
                return JsonResponse(result)
            list_item = ['MerchantID', 'MerchantTradeNo', 'PaymentDate', 'PaymentType', 'PaymentTypeChargeFee',
                         'RtnCode', 'RtnMsg', 'SimulatePaid', 'StoreID', 'TradeAmt', 'TradeDate', 'TradeNo']
            check_origin = 'HashKey=%s&CustomField1=&CustomField2=&CustomField3=&CustomField4=&' % HashKey
            for i in range(len(list_item)):
                get = request.POST.get(list_item[i], '')
                if i == len(list_item) - 1:
                    check_origin += list_item[i] + '=' + str(get) + ("&HashIV=%s" % HashIV)
                else:
                    check_origin += list_item[i] + '=' + str(get) + "&"
            # print(check_encode(check_origin))
            CheckMacValue_o = check_encode(check_origin)
            CheckMac_get = request.POST.get('CheckMacValue', None)
            # print(CheckMac_get)
            RtnCode = request.POST.get('RtnCode', 0)
            # 務必判斷交易狀態[RtnCode]是否為1，若非1 時請勿對該筆交易做出貨動作，並取得交易訊息[RtnMsg] 記錄失敗原因。
            if RtnCode == "1":
                print('交易成功')
                if CheckMac_get == CheckMacValue_o:
                    orders = OrdersFiles.objects.filter(num_list=list_num)
                    if not orders:
                        result = {'code': 400, 'error': 'please give me data'}
                        return JsonResponse(result)
                    try:
                        orders[0].status = 1
                        orders[0].save()
                    except:
                        result = {'code': 500, 'error': 'System is busy'}
                        return JsonResponse(result)
                    return HttpResponse('1|OK')
            else:
                result = {'code': 400, 'error': 'the deal does not success'}
                return JsonResponse(result)
        else:
            result = {'code': 400, 'error': 'please use post method'}
            return JsonResponse(result)
