from django.db import models
from product.models import ProductProfile
from order.models import OrdersFiles
from user.models import UserProfile


# Create your models here.

class OrderList(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(verbose_name='商品數量')
    product = models.ForeignKey(ProductProfile, on_delete=models.CASCADE)
    pprice = models.IntegerField()
    num_list = models.ForeignKey(OrdersFiles, on_delete=models.CASCADE)

    class Meta:
        db_table = 'orderlists'
