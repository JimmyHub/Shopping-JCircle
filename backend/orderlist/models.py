from django.db import models
from product.models import ProductProfile
from order.models import OrdersFiles
from user.models import UserProfile
# Create your models here.

class OrderList(models.Model):
    count = models.IntegerField(verbose_name='εεζΈι') 
    product=models.ForeignKey(ProductProfile,on_delete=models.CASCADE)
    num_list=models.ForeignKey(OrdersFiles,on_delete=models.CASCADE)
    class Meta:
        db_table='orderlists'