from drf_yasg import openapi
from rest_framework import serializers
from .serializers import RegisterSerializer, UserSerializer


class ResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()


class UserGETSerializer(ResponseSerializer):
    data = UserSerializer()


class UserPOSTSerializer(ResponseSerializer):
    data = RegisterSerializer()


class UserPATCHSerializer(ResponseSerializer):
    pass


users_get_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=UserGETSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }

users_post_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=UserPOSTSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }
users_patch_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=UserPATCHSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }
# users_delete_response = {
#     "200": openapi.Response(
#         description="custom 200 description",
#         schema=UserDELETESerializer,
#     ),
#     "400": openapi.Response(
#         description="custom 400 description",
#         schema=ResponseSerializer,
#     ),
# }


users_response_dict = {
    "GET": users_get_response,
    "POST": users_post_response,
    "PATCH": users_patch_response,
    # "DELETE": users_delete_response,
}


class TokenSerializer(serializers.Serializer):
    username =serializers.CharField()
    token = serializers.CharField()

class LoginPOSTSerializer(ResponseSerializer):
    data = TokenSerializer()

login_response = {
    "200": openapi.Response(
        description="custom 200 description",
        schema=LoginPOSTSerializer,
    ),
    "400": openapi.Response(
        description="custom 400 description",
        schema=ResponseSerializer,
    ),
    "403": openapi.Response(
        description="custom 403 description",
        schema=ResponseSerializer,
    ),
}

login_response_dict = {
    "POST": login_response,

}
