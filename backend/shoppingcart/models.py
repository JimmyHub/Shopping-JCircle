from django.db import models

from product.models import ProductProfile
from user.models import UserProfile


class ShoppingList(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(verbose_name='商品數量')
    #刪除 商品 或是 賣家不存在時 購物車的內容也會不見
    product = models.ForeignKey(ProductProfile,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    class Meta:
       db_table='shoppinglists'