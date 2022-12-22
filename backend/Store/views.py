import jwt
import time
import math
import hashlib
import urllib.parse

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from user.models import UserProfile
from user.serializers import UserSerializer
from Store.decorator import allmethods, trycatch

from order.models import OrdersFiles

from .authentication import TokenExAuthentication

IP = 'http://127.0.0.1'
PORT = 8080
key = 'a123456'
# 綠界API
url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'


class IndexView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenExAuthentication, ]

    def get(self, request):
        auser = request.user
        if hasattr(request.user,'limit'):
            result = {'code': status.HTTP_200_OK, 'data': {'username': auser.username,
                                            'avatar': str(auser.avatar),
                                            'limit': auser.limit}}
            return Response(data=result)
        else:
            result = {'code': status.HTTP_200_OK, 'data': 'nouser'}
            return Response(data=result)



# CheckMacValue 驗證碼生成
def checkvalue_encode(origin):
    # 1.urlencode
    origin_encode = urllib.parse.quote(origin)
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


@allmethods(trycatch)
class EcpayTrade(GenericAPIView):
    queryset = OrdersFiles.objects.all()

    def __init__(self):
        self.hash_key = '5294y06JbISpM5x9'
        self.hash_iv = 'v77hoKGq4kWxNNIS'

    def checkvalue_make(self, item_dict):
        check_list = [f'{k}={v}' for k, v in item_dict.items()]
        check_origin = '&'.join(check_list)
        CheckMacValue = checkvalue_encode(check_origin)
        return CheckMacValue

    # 驗證碼生成  前置數據生成
    def ecpay_jc(self, list_num):
        # 透過order id 從現有OrdersFiles 數據庫 拿數據出來

        orders = OrdersFiles.objects.filter(num_list=list_num)
        if not orders:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'This list does not exist'}
            return Response(data=result)
        if orders[0].payway == 1:
            ChoosePayment = 'Credit'
        elif orders[0].payway == 2:
            ChoosePayment = 'BARCODE'
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 透過API獲得參數數值後，根據參數查找資料庫的數據，直接用資料庫內查到的值作替代
        list_num_db = orders[0].num_list
        item_dict = {
            'HashKey': self.hash_key,
            'ChoosePayment': ChoosePayment,
            'ClientBackURL': f'{IP}:{PORT}/#/orders',
            'EncryptType': 1,
            'ItemName': 'jCircle商品一組',
            'MerchantID': '2000132',
            'MerchantTradeDate': orders[0].num_time[0:10] + ' ' + orders[0].num_time[11:19],
            'MerchantTradeNo': 'jCircle' + str(list_num_db),
            'OrderResultURL': f'{IP}:{PORT}/#/orders',
            'PaymentType': 'aio',
            'ReturnURL': 'http://www.jcircle.ml/api/v1/CheckMacValue/' + str(list_num_db),
            'TotalAmount': orders[0].money_total,
            'TradeDesc': 'JCshoppingmall',
            # IV加尾吧
            'HashIV': self.hash_iv}
        return self.checkvalue_make(item_dict)

    # 訂單繳費成立回調

    def check_pay_already(self, request, list_num):
        if request.method == 'POST':
            if not list_num:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'please give me list_num'}
                return Response(data=result)
            item_dict = {
                'HashKey': self.hash_key,
                'CustomField1': '',
                'CustomField2': '',
                'CustomField3': '',
                'CustomField4': '',
                'MerchantID': '',
                'MerchantTradeNo': '',
                'PaymentDate': '',
                'PaymentType': '',
                'PaymentTypeChargeFee': '',
                'RtnCode': '',
                'RtnMsg': '',
                'SimulatePaid': '',
                'StoreID': '',
                'TradeAmt': '',
                'TradeDate': '',
                'TradeNo': '',
                'HashIV': self.hash_iv
            }
            for item in item_dict:
                item_dict[item] = request.POST.get(item, '')
            checkvalue_old = self.checkvalue_make(item_dict)
            checkvalue_get = request.POST.get('CheckMacValue', None)
            RtnCode = request.POST.get('RtnCode', 0)
            # 務必判斷交易狀態[RtnCode]是否為1，若非1 時請勿對該筆交易做出貨動作，並取得交易訊息[RtnMsg] 記錄失敗原因。
            if RtnCode == '1':
                print('交易成功')
                if checkvalue_get == checkvalue_old:
                    # product = get_object_or_404(OrdersFiles, id=pk)
                    orders = OrdersFiles.objects.filter(num_list=list_num)
                    if not orders:
                        result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'please give me data'}
                        return Response(data=result)
                    orders[0].status = 1
                    orders[0].save()
                    return HttpResponse('1|OK')
            else:
                result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'the deal does not success'}
                return Response(data=result)
        else:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'please use post method'}
            return Response(data=result)

    # 訂單創建成立查詢
    def ordercheck(self, request, list_num):
        if not list_num:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'please give me list number'}
            return Response(data=result)
        orders = OrdersFiles.objects.filter(num_list=list_num)
        if not orders:
            result = {'code': status.HTTP_400_BAD_REQUEST, 'error': 'This order don`t exist'}
            return Response(data=result)
        item_dict = {
            'HashKey': self.hash_key,
            'MerchantID': '2000132',
            'MerchantTradeNo': 'jCircle' + str(orders[0].num_list),
            'TimeStamp': math.floor(time.time()),
            'HashIV': self.hash_iv,
        }
        CheckMacValue = self.checkvalue_make(item_dict)
        result = {'code': status.HTTP_200_OK, 'data': {'check': CheckMacValue, 'time': item_dict['TimeStamp']}}
        return Response(data=result)


Ecpay = EcpayTrade()
