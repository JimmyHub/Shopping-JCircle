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
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from tools import Ecpay
from . import views

urlpatterns=[
    url(r'^admin/', admin.site.urls),
    url(r'v1/index$',views.index),
    url(r'v1/users',include('user.urls')),
    url(r'v1/products',include('product.urls')),
    url(r'v1/shoppings',include('shoppingcart.urls')),
    url(r'v1/orders',include('order.urls')),
    url(r'v1/orderlists',include('orderlist.urls')),
    url(r'v1/messages',include('message.urls')),
    url(r'v1/CheckMacValue/(?P<list_num>[\w]{1,11})',Ecpay.CheckMacValue),
    url(r'v1/orderCheck/(?P<list_num>[\w]{1,11})',Ecpay.orderCheck)
]
#生成媒體資源路由
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)