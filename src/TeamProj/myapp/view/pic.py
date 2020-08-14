from django.contrib.auth.hashers import make_password

from myapp.models import User, UserToken, EmailRecord
from myapp.serializers import UserInfoSer
from myapp.views import md5, random_str
from rest_framework.views import APIView, Response
from django.conf import settings
from django.core.mail import send_mail
import datetime
import os,json
from django.utils import timezone   # 获取当前时间
import hashlib   # 给当前时间编码

count=1

# 发往：/picSave
# 返回：/picSave/filename.
# 用来接收前端文本编辑发送上来的文件
class getPic(APIView):
    def post(self,request):
        myFile = request.FILES.get("image", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return Response("no files for upload!")    
        time_now = timezone.now()  # 获取当前日期时间
        # 2019-04-03 00:51:21.225391+00:00 time_now当前打印的时间格式是这样，不能直接使用，需要用MD5编码
        m = hashlib.md5()
        m.update(str(time_now).encode())   # 给当前时间编码
        time_now = m.hexdigest()
        print(time_now)  # ec3b25c7e44ded02d092c57dded2d5eb  此时为编码后的时间
        destination = open(os.path.join(settings.MEDIA_ROOT, time_now+myFile.name),'wb+')
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()
        #print(os.path.join("E:\\upload", time_now+myFile.name))
        return Response({
                'info': '上传成功',
                'code': 200,
                'url': time_now + myFile.name
            }, status=200)    
