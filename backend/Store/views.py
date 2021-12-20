from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from user.models import UserProfile
import jwt
key='a123456'

def index(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        if token == "null":
            print(token)
            result={'code':200,'data':'nouser'}
            return JsonResponse(result)
        else:
            print(token,'1')    
            try:
                token_de=jwt.decode(token,key,algorithms=['HS256'])
            except jwt.ExpiredSignatureError as e :
                result={'code':401,'error':'please login one more time!'}
                return JsonResponse(result)
            username_de=token_de['username']
            auser = UserProfile.objects.filter(name=username_de)
            if not auser:
                result={'code':410,'error':'This user do not exist !'}
                return JsonResponse(result)
            if auser[0].name:
                username = auser[0].name
                avatar = str(auser[0].avatar)
                limit= auser[0].limit
                result={'code':200,'data':{"username":username,
                                           "avatar":avatar,
                                           "limit":limit}}
                return JsonResponse(result)
            else:
                result={'code':410,'error':'This user do not exist !'}
                return JsonResponse(result)