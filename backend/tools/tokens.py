import jwt,time
from django.http import JsonResponse
from user.models import UserProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

key='a123456'
def make_token(username,expire=3600*24):
    #生成token 返回給前端
    now=time.time()
    limit_time=now+expire
    payload={'username':username,'exp':limit_time}
    return jwt.encode(payload,key,algorithm='HS256')

def auth_swagger_wrapper(summary,description):
    return swagger_auto_schema(
        operation_summary=summary,
        operation_description=description,
        manual_parameters=[
            openapi.Parameter(
                name='HTTP_AUTHORIZATION',
                required=True,
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
            )
        ]
    )

def login_check(*method):
    # 判斷是否有登錄
    def _login_check(func):
        def wrapper(obj,*args,**kwargs):
            request = obj.request
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
            # print('name:',name)
            # print(request.session.values())
            users = UserProfile.objects.filter(username=name)
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
