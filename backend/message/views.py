from django.http import JsonResponse
from tools.tokens import login_check
from .models import MessageRecord
import json
# Create your views here.

@login_check('GET','POST')
def messages(request,keyword=None):
    if request.method=='GET':
        if keyword == None:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        msgs = MessageRecord.objects.filter(num_list_id=keyword)
        if not msgs:
        	result={'code':200,'data':'norecord'}
        	return JsonResponse(result)
        msg_list=[]
        for i in msgs:
            dic_msg={
                'content':i.content,
                'con_time':i.content_time,
                'user':i.user_id,
            }
            msg_list.append(dic_msg)
        result={'code':200,'data':msg_list}
        return JsonResponse(result)


    elif request.method=='POST':
        if keyword == None:
            result={'code':400,'error':'please give me keyword'}
            return JsonResponse(result)
        json_str=request.body
        if not json_str:
            result={'code':400,'error':'please give data'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        content=json_obj.get('content')
        if not content:
            result={'code':400,'error':'please give content'}
            return JsonResponse(result)
        try:
            MessageRecord.objects.create(content=content,
                                         user_id=request.user.username,
                                         num_list_id=keyword)
        except:
            result={'code':500,'error':'System is busy'}
            return JsonResponse(result)
        new_msg=MessageRecord.objects.filter(num_list_id=keyword).order_by('-id')
        if not new_msg:
            result={'code':400,'error':'Something must be wrong'}
            return JsonResponse(result)  
        fresh_msg={
            'content':new_msg[0].content,
            'con_time':new_msg[0].content_time,
            'user':new_msg[0].user.username,
        }
        result={'code':200,'data':fresh_msg}
        return JsonResponse(result) 	
