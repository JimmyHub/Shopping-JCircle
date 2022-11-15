import inspect
import functools

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def allmethods(decorator):
    @functools.wraps(decorator)
    def dectheclass(cls):
        for name, m in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, decorator(m))
        return cls

    return dectheclass


def make_validationerror_msg(ve_dict,ve_list):
    for item, msg in ve_dict.items():
        if isinstance(msg, dict):
            make_validationerror_msg(msg, ve_list)
        else:
            ve_list.append(f'{item}_field: {str(msg[0])}')
    return ve_list


@transaction.atomic
def trycatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except ValidationError as ve:
            ve_res = make_validationerror_msg(ve.__dict__['detail'],[])
            result = {'status': status.HTTP_400_BAD_REQUEST, 'message': f'{" ,".join(ve_res)}'}
            return Response(data=result)

        except KeyError as ke:
            result = {'status': status.HTTP_400_BAD_REQUEST,
                      'message': f'The word {ke} you passed in request maybe be wrong or your serializer maybe wrong'}
            return Response(data=result)

        except Exception as e:
            result = {'status': status.HTTP_400_BAD_REQUEST, 'message': f'{e}'}
            return Response(data=result)

    return wrapper


def request_response(response_schema_dict, query=True):
    def token_query(func):
        if query:
            @functools.wraps(func)
            @swagger_auto_schema(
                # request_body=request_schema,
                responses=response_schema_dict,
                manual_parameters=[
                    openapi.Parameter(
                        name='HTTP_AUTHORIZATION',
                        in_=openapi.IN_HEADER,
                        type=openapi.TYPE_STRING
                    )
                ]
            )
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
        else:
            @functools.wraps(func)
            @swagger_auto_schema(
                responses=response_schema_dict,
            )
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
        return wrapper
    return token_query
