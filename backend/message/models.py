from django.db import models
from user.models import UserProfile
from order.models import OrdersFiles
# Create your models here.
class MessageRecord(models.Model):
	content = models.TextField(verbose_name='留言內容')
	content_time=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	num_list=models.ForeignKey(OrdersFiles,on_delete=models.CASCADE)
	class Meta:
		db_table='messages'