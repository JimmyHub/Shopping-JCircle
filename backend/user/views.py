from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Store.decorator import allmethods, trycatch, request_response
from Store.authentication import TokenExAuthentication
from Store.tool import get_json_data, get_serializer_data

from .models import UserProfile
from .response_schema import users_response_dict, login_response_dict
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer



@allmethods(trycatch)
class UsersViewSet(GenericViewSet):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenExAuthentication, ]

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return RegisterSerializer
        else:
            return UserSerializer

    # 帳號資料瀏覽
    @request_response(response_schema_dict=users_response_dict['GET'], query=True)
    def get_user(self, request):
        data_res = UserSerializer(request.user)
        data_res.data['avatar'] = str(data_res.data['avatar'])
        result = {'code': status.HTTP_200_OK, 'data': data_res.data}
        return Response(data=result)

    # 帳號註冊
    @request_response(response_schema_dict=users_response_dict['POST'])
    def create(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data, request)
        self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_201_CREATED, 'data': {'username': self.serializer.validated_data['username']}}
        return Response(data=result)

    # 修改個人資料
    @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)
        get_serializer_data(self, data, request, partial=True)
        self.serializer.update(instance=request.user, data=self.serializer.validated_data)
        result = {'code': status.HTTP_202_ACCEPTED}
        return Response(data=result)


@allmethods(trycatch)
class UserAvatarView(GenericViewSet):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenExAuthentication, ]
    parser_classes = (MultiPartParser,)

    @request_response(response_schema_dict=users_response_dict['POST'])
    def create(self, request):
        avatar = request.FILES.get('avatar')
        auser = request.user
        auser.avatar = avatar
        auser.save()
        result = {'code': status.HTTP_201_CREATED}
        return Response(data=result)

        # drf 存圖片 ??
        # 上傳用戶頭像
        # 從網頁中獲取 上傳的圖片或文件 用 request.FILES['標籤name名稱']
        # 從網頁中獲取 json資料的話 則是使用 request.DATA
        # print(request.FILES.get('avatar'))
        # print(request.data)
        # get_serializer_data(self,request.data,request)
        # self.serializer.update(instance=request.user, data=self.serializer.validated_data)
        # result = {'code': 200, 'username': request.user.username}
        # # return render(request, 'user/info.html', locals())
        # return Response(result)
        # if not avatar:
        #     result = {'code': 400, 'error': 'I need avatar'}
        #     return JsonResponse(result)
        # # 作業:判斷url中的username 跟token中的username是否一致 否則返回error

        # return render(request,'user/info.html',locals())
        # 如果上傳自動更新之後 圖片沒有出現 可以先查看圖片地址為何
        # 然後查看 請求中的響應 是否有正確get到數據


@allmethods(trycatch)
class LoginViewSet(GenericViewSet):
    queryset = UserProfile
    serializer_class = LoginSerializer

    @request_response(response_schema_dict=login_response_dict['POST'], query=False)
    def login(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data=data, request=request)
        data_valid = self.serializer.validated_data
        result = {'code': 200, 'data': {'username': data_valid['username'], 'token': data_valid['token']}}
        return Response(result)
