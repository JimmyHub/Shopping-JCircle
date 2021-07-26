import requests
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
# Create your views here.
import json
from .models import UserProfile
import hashlib

from tools.tokens import login_check,make_token
key='a123456'
@login_check('PUT','GET')
def users(request):
    #帳號資料瀏覽
    if request.method == 'GET':
        auser = request.user
        if not auser:
            #將訪問者的username跟數據庫做比對
            #如果沒有比對到對象就導向登入頁面
            result={'code':400,'error':'No user!'}
            return JsonResponse(result)
        name=auser.name
        birthday=auser.birthday
        gender=auser.gender
        phone=auser.phone
        email=auser.email
        avatar=str(auser.avatar)
        limit=auser.limit
        result={'code':200,'data':{'username':name,
                                   'birthday':birthday,
                                   'gender':gender,
                                   'phone':phone,
                                   'email':email,
                                   'avatar':avatar,
                                   'limit':limit}}
        return JsonResponse(result)
        #return render(request,'user/info.html',locals())

    #帳號註冊
    elif request.method == 'POST':
        json_str= request.body
        if not json_str:
            #若沒有傳數據過來 就返回錯誤 201 請輸入資料
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        name = json_obj.get('username')
        if not name:
            reult={'code':400,'error':'please give me name'}
            return JsonResponse(reult)
        if len(name) < 5 :
            reult={'code':400,'error':'please give me over 5 words (name)'}
            return JsonResponse(reult)
        password=json_obj.get('pwd1')
        if not password:
            result={'code':400,'error':'please give me password'}
            return JsonResponse(result)
        if len(password)<5:
            reult={'code':400,'error':'please give me over 5 words (password)'}
            return JsonResponse(reult)
        password2 = json_obj.get('pwd2')
        if password2 != password:
            result = {'code':400,'error':'please enter same code'}
            return JsonResponse(result)
        phone = json_obj.get('phone')
        if not phone :
            result ={'code':400,'error':'please give me phone number'}
            return JsonResponse(result)
        if len(phone) != 10:
            reult={'code':400,'error':'please give me correct numder'}
            return JsonResponse(reult)
        email = json_obj.get('email')
        if not email:
            result = {'code':400,'error':'please give me email'}
            return JsonResponse(result)
        user=UserProfile.objects.filter(name=name)
        if user:
            result={'code':400,'error':'This username is exist'}
            return JsonResponse(result)
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
        result = {'code': 200,'data': {'username': name,'token': token}}
        return JsonResponse(result)

    #修改個人資料
    elif request.method == 'PUT':
        #其他基本資料上傳
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give me data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        #獲取傳過來的data看世傳過來哪一種 對其項目進行修改
        auser = request.user
        key=[]
        for i in json_obj:
            key.append(i)
        print(key)
        if len(key) == 2:
            password_old = json_obj.get(key[0], 0)
            m = hashlib.md5()
            m.update(password_old.encode())
            p_old = m.hexdigest()
            print(password_old)
            if p_old != auser.password:
                result={'code':400,'error':'please enter correct old password'}
                return JsonResponse(result)
            password_new = json_obj.get('password_n', 0)
            print(password_new)
            if password_old == password_new:
                result = {'code': 400, 'error': 'please enter different  password'}
                return JsonResponse(result)
            n=hashlib.md5()
            n.update(password_new.encode())
            p_new = n.hexdigest()
            auser.password=p_new
            print('ok')
        else:
            value = json_obj.get(key[0], 0)
            if key[0] == 'birthday':
                auser.birthday = value
            elif key[0] == 'gender':
                if value not in ('Male','Female'):
                    result={'code':400,'error':'please enter correct option'}
                    return JsonResponse(result)
                auser.gender = value
            elif key[0] == 'phone':
                if len(value) !=10:
                    result = {'code': 400, 'error': 'please enter correct phone number'}
                    return JsonResponse(result)
                auser.phone = value
            elif key[0] == 'email':
                auser.email = value
        auser.save()
        result = {'code': 200, 'username':auser.name}
        return JsonResponse(result)
    else:
        result={'code':400,'error':'code must be wrong'}
        return  JsonResponse(result)

@login_check('POST')
def user_avatar(request):
    # 上傳用戶頭像
    if request.method != 'POST':
        result = {'code': 405, 'error': 'I need post'}
        return JsonResponse(result)
    # 從網頁中獲取 上傳的圖片或文件 用 request.FILES['標籤name名稱']
    # 從網頁中獲取 json資料的話 則是使用 request.DATA
    avatar = request.FILES.get('avatar')
    if not avatar:
        result = {'code': 400, 'error': 'I need avatar'}
        return JsonResponse(result)
    # 作業:判斷url中的username 跟token中的username是否一致 否則返回error
    auser = request.user
    auser.avatar = avatar
    auser.save()
    result = {'code': 200, 'username': auser.name}
    #return render(request, 'user/info.html', locals())
    return JsonResponse(result)
    #return render(request,'user/info.html',locals())
    # 如果上傳自動更新之後 圖片沒有出現 可以先查看圖片地址為何
    # 然後查看 請求中的響應 是否有正確get到數據


