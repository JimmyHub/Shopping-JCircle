from django.db import models
from user.models import UserProfile
# Create your models here.


class ProductProfile(models.Model):
    pname = models.CharField(verbose_name='商品名稱',max_length=30)
    pkind = models.CharField(verbose_name='商品種類',max_length=30)
    pphoto = models.ImageField(verbose_name='商品圖片',upload_to='product/')
    pcontent = models.TextField(verbose_name='商品內容')
    pprice = models.IntegerField(verbose_name='商品金額')
    pway = models.IntegerField(verbose_name='付款方式')
    #當賣家不存在的時候 商品也會跟著消失
    sales = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    class Meta:
        db_table = 'products'