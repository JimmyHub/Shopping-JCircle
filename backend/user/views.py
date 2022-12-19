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
        get_serializer_data(self, data)
        self.serializer.create(self.serializer.validated_data)
        result = {'code': status.HTTP_201_CREATED, 'data': {'username': self.serializer.validated_data['username']}}
        return Response(data=result)

    # 修改個人資料
    @request_response(response_schema_dict=users_response_dict['PATCH'])
    def partial_update(self, request, pk=None):
        data = get_json_data(request.body)
        get_serializer_data(self, data, partial=True)
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


@allmethods(trycatch)
class LoginViewSet(GenericViewSet):
    queryset = UserProfile
    serializer_class = LoginSerializer

    @request_response(response_schema_dict=login_response_dict['POST'], query=False)
    def login(self, request):
        data = get_json_data(request.body)
        get_serializer_data(self, data)
        data_valid = self.serializer.validated_data
        result = {'code': 200, 'data': {'username': data_valid['username'], 'token': data_valid['token']}}
        return Response(result)
