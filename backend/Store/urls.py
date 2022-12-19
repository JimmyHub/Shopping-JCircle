from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator


from . import views
from user.views import UsersViewSet
from .views import EcpayTrade

from product.views import ProductViewSet


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
    path('v1/users', include('user.urls')),
    path('v1/index', views.IndexView.as_view()),
    path('v1/products', include('product.urls')),
    path('v1/shoppings', include('shoppingcart.urls')),
    path('v1/orders', include('order.urls')),
    path('v1/orderlists', include('orderlist.urls')),
    # path('v1/messages',include('message.urls')),
    path('v1/CheckMacValue/<int:list_id>', EcpayTrade.check_pay_already),
    path('v1/orderCheck/<int:keyword>', EcpayTrade.ordercheck),

]
urlpatterns += [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# 生成媒體資源路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
