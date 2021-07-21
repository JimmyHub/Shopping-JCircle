from django.db import models
from user.models import UserProfile
# Create your models here.

class OrdersFiles(models.Model):
    num_list=models.IntegerField(verbose_name='訂單編號')
    num_time=models.CharField(verbose_name='訂單時間',max_length=30)
    status=models.IntegerField(verbose_name='訂單狀態')
    #訂單狀態改變的時候 紀錄時間
    status_time=models.DateTimeField(auto_now=True)
    gname=models.CharField(verbose_name='收貨人',max_length=20)
    address=models.CharField(verbose_name='地址',max_length=30)
    phone=models.CharField(verbose_name='電話',max_length=20)
    payway=models.IntegerField(verbose_name='付款方式')
    content=models.CharField(verbose_name='備註',max_length=30)
    bonus=models.IntegerField(verbose_name='優惠')
    shipping=models.IntegerField(verbose_name='運費')
    money_total=models.IntegerField(verbose_name='總金額')
    buyer=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='buyer')
    sales=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='sales')
    class Meta:
    	  db_table='orders'