import hashlib
import json

import jwt,time
from django.http import JsonResponse
from django.shortcuts import render
from user.models import UserProfile
key='a123456'
def make_token(username,expire=3600*24):
    #生成token 返回給前端
    now=time.time()
    limit_time=now+expire
    payload={'username':username,'exp':limit_time}
    return jwt.encode(payload,key,algorithm='HS256')

def login_check(*method):
    # 判斷是否有登錄
    def _login_check(func):
        def wrapper(request,*args,**kwargs):
            #判斷 請求方法是否為標記中的方法
            if request.method not in method:
                return func(request, *args, **kwargs)
            #判斷是否在網頁中有token
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token :
                result={'code':401,'error':'please login!'}
                return JsonResponse(result)
            #如果有token 將token解密
            #因為有設置token的時效 所以要確定token是否有過期
            #有過期會抱錯 所以要進行try避免中斷
            try:
                token_de=jwt.decode(token,key,algorithms=['HS256'])
            except jwt.ExpiredSignatureError as e :
                result={'code':401,'error':'please login one more time!'}
                return JsonResponse(result)
            #或是解密出來 不正確也要中斷
            except Exception as e:
                result = {'code':401,'error':'please login'}
                return JsonResponse(result)
            name = token_de['username']
            users = UserProfile.objects.filter(name=name)
            #判斷解密出來的user是否存在數據庫中
            if not users:
                result={'code':410,'error':'This user do not exist!'}
                return JsonResponse(result)
            #如果存在數據庫中,就將數據儲存到request裡面 然後返回
            request.user = users[0]
            return func(request, *args, **kwargs)
            #將解密的token中的username拿出來跟 個人資料數據庫中的資料庫做對比
        return wrapper
    return _login_check

def login(request):
    if request.method == 'POST':
        #從request中獲取資料
        json_str = request.body
        if not json_str:
            result={'code':400,'error':'please give me data.'}
            return JsonResponse(result)
        #將資料轉換成字典
        json_obj = json.loads(json_str)
        #獲取字典裡的資料
        name = json_obj.get('username')
        #檢查有沒有輸入username
        if not name:
            result={'code':400,'error':'please enter username.'}
            return JsonResponse(result)
        pwd=json_obj.get('pwd')
        print(pwd)
        if not pwd:
            print('no pwd')
            result={'code':400,'error':'please enter password.'}
            return JsonResponse(result)
        #將資料跟數據庫資料進行比對
        user = UserProfile.objects.filter(name=name)
        if not user:
            result={'code':410,'error':'This user do not exist!'}
            return JsonResponse(result)
        auser = user[0]
        m=hashlib.md5()
        m.update(pwd.encode())
        p_get=m.hexdigest()
        if auser.password != p_get:
            result={'code':400,'error':'The password is wrong'}
            return JsonResponse(result)
        token_login=make_token(name)
        print(token_login)
        result={'code':200,'data':{'username':name,'token':token_login}}
        return JsonResponse(result)
    else:
        result={'code':405,'error':'This is not correct way.'}
        return JsonResponse(result)
