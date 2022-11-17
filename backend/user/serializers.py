import hashlib
import time

import jwt
from rest_framework.generics import get_object_or_404

from .models import UserProfile
from rest_framework import serializers


def make_complicate(password):
    m = hashlib.md5()
    m.update(password.encode())
    pwd_final = m.hexdigest()
    return pwd_final


def make_token(username, expire=3600 * 24):
    # 生成token 返回給前端
    now = time.time()
    limit_time = now + expire
    payload = {'username': username, 'exp': limit_time}
    return jwt.encode(payload, key='a123456', algorithm='HS256')


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5)
    phone = serializers.CharField(min_length=10)
    email = serializers.CharField()


class RegisterSerializer(UserBaseSerializer):
    pwd1 = serializers.CharField(min_length=5)
    pwd2 = serializers.CharField(min_length=5)

    def validate_phone(self, value):
        if len(value) >= 11:
            raise SystemError("手機號碼長度錯誤")
        return value

    def validate(self, data):
        if data['username'] in data['pwd1']:
            raise SystemError("密碼跟帳號太過相似")
        pwd1, pwd2 = data.pop('pwd1'), data.pop('pwd2')
        if pwd1 != pwd2:
            raise SystemError("重複密碼輸入錯誤")
        data['password'] = make_complicate(pwd1)
        return data

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer, RegisterSerializer):
    birthday = serializers.CharField(default=' ')
    gender = serializers.CharField(default=' ')
    avatar = serializers.ImageField(use_url="media/")
    limit = serializers.IntegerField(default=1)

    class Meta:
        model = UserProfile
        fields = ('username', 'birthday', 'phone', 'gender', 'email', 'avatar', 'limit',)

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    def validate_birthday(self, value):
        value_get = value.split('/')
        for v in value_get:
            try:
                int(v)
            except:
                raise SystemError("輸入內容錯誤")

        if len(value_get) != 3:
            raise SystemError("生日格式錯誤")
        if len(value_get[0]) != 4 or len(value_get[1]) != 2 or len(value_get[2]) != 2:
            raise SystemError("生日格式錯誤")
        else:
            return value

    def validate(self, data):
        return data

    def update(self, instance, data):
        user_queryset = UserProfile.objects.get(pk=instance.username)
        UserProfile.objects.filter(pk=instance.username) \
            .update(**data)
        return user_queryset


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5)
    pwd = serializers.CharField(min_length=5)

    def validate(self, data):
        user = get_object_or_404(UserProfile,username =data['username'])

        if make_complicate(data['pwd']) != user.password:
            raise SystemError("輸入密碼錯誤")
        data['token'] = make_token(user.username)
        return data

# class AvatarSerializer(serializers.Serializer):
#     avatar = serializers.ImageField(use_url="media/",)
#
#     def update(self, instance, data):
#         user_queryset = UserProfile.objects.get(pk=instance.username)
#         UserProfile.objects.filter(pk=instance.username) \
#             .update(**data)
#
#         return user_queryset
