from django.db import models


# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(verbose_name='用戶名', max_length=11, primary_key=True)
    password = models.CharField(verbose_name='密碼', max_length=32)
    birthday = models.CharField(verbose_name='生日', max_length=10, null=True)
    phone = models.CharField(verbose_name='電話', max_length=11)
    gender = models.CharField(verbose_name='性別', max_length=8, null=True)
    email = models.CharField(verbose_name='信箱', max_length=50)
    avatar = models.ImageField(verbose_name='頭像', upload_to='avatar/')
    limit = models.IntegerField(verbose_name='權限', default=1)

    class Meta:
        db_table = 'users'  # 可以更改在數據庫中的顯示
