import json
import hashlib
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tools.tokens import login_check, make_token
from Store.decorator import allmethods, trycatch
from Store.authentication import TokenExAuthentication

from .models import UserProfile
from .serializers import UserSerializer, RegisterSerializer


@allmethods(trycatch)
class UsersView(GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenExAuthentication, ]

    def get_serializer_data(self, serializer, request):
        self.serializer = serializer(data=request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)

    # 帳號資料瀏覽
    def retrieve(self, request):
        data_res = UserSerializer(request.user)
        # data_res = model_to_dict(user)
        # avatar = str(auser.avatar)
        result = {'code': status.HTTP_200_OK, 'data': data_res.data}
        return Response(data=result)

    # 帳號註冊
    def create(self, request):
        self.get_serializer_data(RegisterSerializer, request)
        self.serializer.create()
        result = {'code': status.HTTP_201_CREATED, 'data': {'username': self.serializer.validated_data['username']}}
        return JsonResponse(result)

    # 修改個人資料
    def partial_update(self, request, pk=None):
        serialized = UserSerializer(request.user, data=request.data, partial=True)
        result = {'code': status.HTTP_202_ACCEPTED, 'username': serialized.data.username}
        return Response(data=result)



class UserAvatarView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @login_check('POST')
    def post(self, request):
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
        result = {'code': 200, 'username': auser.username}
        # return render(request, 'user/info.html', locals())
        return JsonResponse(result)
        # return render(request,'user/info.html',locals())
        # 如果上傳自動更新之後 圖片沒有出現 可以先查看圖片地址為何
        # 然後查看 請求中的響應 是否有正確get到數據


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
    result = {'code': 200, 'username': auser.username}
    # return render(request, 'user/info.html', locals())
    return JsonResponse(result)
    # return render(request,'user/info.html',locals())
    # 如果上傳自動更新之後 圖片沒有出現 可以先查看圖片地址為何
    # 然後查看 請求中的響應 是否有正確get到數據
