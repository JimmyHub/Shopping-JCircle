from drf_yasg import openapi
from .serializers import MemberGETSerializer, MemberPOSTSerializer, MemberPUTSerializer, MemberDELETESerializer, \
    MemberLOOKUPSerializer, LoginPOSTSerializer, LoginCHECKSerializer, LoginOUTSerializer, ResponseSerializer

memebers_get_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=MemberGETSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }

memebers_post_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=MemberPOSTSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }
memebers_put_response = \
    {
        "200": openapi.Response(
            description="custom 200 description",
            schema=MemberPUTSerializer,
        ),
        "400": openapi.Response(
            description="custom 400 description",
            schema=ResponseSerializer,
        ),
    }
memebers_delete_response = {
    "200": openapi.Response(
        description="custom 200 description",
        schema=MemberDELETESerializer,
    ),
    "400": openapi.Response(
        description="custom 400 description",
        schema=ResponseSerializer,
    ),
}
memebers_lookup_response = {
    "200": openapi.Response(
        description="custom 200 description",
        schema=MemberLOOKUPSerializer,
    ),
    "400": openapi.Response(
        description="custom 400 description",
        schema=ResponseSerializer,
    ),
}

memebers_response_dict = {
    "GET": memebers_get_response,
    "POST": memebers_post_response,
    "PUT": memebers_put_response,
    "DELETE": memebers_delete_response,
    "LOOKUP": memebers_lookup_response,
}

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
logincheck_response = {
    "200": openapi.Response(
        description="custom 200 description",
        schema=LoginCHECKSerializer,
    ),
    "400": openapi.Response(
        description="custom 400 description",
        schema=ResponseSerializer,
    ),
}
logout_response = {
    "200": openapi.Response(
        description="custom 200 description",
        schema=LoginOUTSerializer,
    ),
    "400": openapi.Response(
        description="custom 400 description",
        schema=ResponseSerializer,
    ),
}
login_response_dict = {
    "LOGIN": login_response,
    "LOGINCHECK": logincheck_response,
    "LOGOUT": logout_response,

}
