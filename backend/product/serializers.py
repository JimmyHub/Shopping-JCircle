from drf_yasg import openapi

from .models import ProductProfile
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductProfile
        fields = "__all__"
        # 這個欄位 的設定部分 會影響在 openapi 的 model 提示有關
        # fields = ('pname', 'pkind', 'pprice')



