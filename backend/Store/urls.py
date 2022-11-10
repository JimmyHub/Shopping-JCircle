"""Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.routers import DefaultRouter
from tools import Ecpay
from . import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# router = DefaultRouter()
# router.register('users',UsersView)


class CustomerGeneratorSchema(OpenAPISchemaGenerator):
    def get_operation(self, *args, **kwargs):
        operation = super().get_operation(*args, **kwargs)
        your_header = openapi.Parameter(
            name='HTTP_AUTHORIZATION',
            description="Description",
            required=True,
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
        )
        operation.parameters.append(your_header)
        return operation


schema_view = get_schema_view(
    openapi.Info(
        title="jCircle API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jimmy.lin@cyan.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # generator_class=CustomerGeneratorSchema
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include(router.urls)),
    path('v1/users', include('user.urls')),
    path('v1/index', views.IndexView.as_view()),
    path('v1/products', include('product.urls')),
    path('v1/shoppings', include('shoppingcart.urls')),
    path('v1/orders', include('order.urls')),
    path('v1/orderlists', include('orderlist.urls')),
    # path('v1/messages',include('message.urls')),
    path('v1/CheckMacValue/<int:list_id>', Ecpay.CheckMacValue),
    path('v1/orderCheck/<int:keyword>', Ecpay.orderCheck),

]
urlpatterns += [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# 生成媒體資源路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
