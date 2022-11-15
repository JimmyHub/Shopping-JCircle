from django.http import JsonResponse, HttpResponse
from rest_framework.generics import GenericAPIView
import jwt

from user.models import UserProfile
from user.serializers import UserSerializer
from tools.tokens import auth_swagger_wrapper
import json
key='a123456'


class IndexView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    @auth_swagger_wrapper('','')
    def get(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == "null":
            result={'code':200,'data':'nouser'}
            return JsonResponse(result)
        else:
            try:
                token_de=jwt.decode(token,key,algorithms=['HS256'])
            except jwt.ExpiredSignatureError as e :
                result={'code':401,'error':'please login one more time!'}
                return JsonResponse(result)
            username_de=token_de['username']
            auser = UserProfile.objects.filter(username=username_de)
            if not auser:
                result={'code':410,'error':'This user do not exist !'}
                return JsonResponse(result)
            if auser[0].username:
                username = auser[0].username
                avatar = str(auser[0].avatar)
                limit= auser[0].limit
                result={'code':200,'data':{"username":username,
                                           "avatar":avatar,
                                           "limit":limit}}
                return JsonResponse(result)
            else:
                result={'code':410,'error':'This user do not exist !'}
                return JsonResponse(result)