import hashlib

from .models import UserProfile
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5)
    phone = serializers.CharField(min_length=10)
    email = serializers.CharField()
    pwd1 = serializers.CharField(min_length=5)
    pwd2 = serializers.CharField(min_length=5)

    def make_complicate(self, password):
        m = hashlib.md5()
        m.update(password.encode())
        pwd_final = m.hexdigest()
        return pwd_final

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("手機號碼長度錯誤")
        return value

    def validate(self, data):
        if data['username'] in data['password']:
            raise serializers.ValidationError("密碼跟帳號太過相似")
        pwd1, pwd2 = data.pop('pwd1'), data.pop('pwd2')
        if pwd1 != pwd2:
            raise serializers.ValidationError("重複密碼輸入錯誤")
        data['password'] = self.make_complicate(pwd1)
        return data

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer, RegisterSerializer):
    birthday = serializers.CharField(default=' ')
    gender = serializers.CharField(default=' ')
    avatar = serializers.ImageField(default=' ')
    limit = serializers.IntegerField(default=0)

    class Meta:
        model = UserProfile
        fields = ('username', 'birthday', 'gender', 'email', 'avatar', 'limit',)

    def update(self, instance, validated_data):
        user_queryset = UserProfile.objects.get(pk=instance.username)
        UserProfile.objects.filter(pk=instance.username)\
                           .update(**validated_data)
        return user_queryset