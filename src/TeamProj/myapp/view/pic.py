from django.contrib.auth.hashers import make_password

from myapp.models import User, UserToken, EmailRecord
from myapp.serializers import UserInfoSer
from myapp.views import md5, random_str
from rest_framework.views import APIView, Response
from django.conf import settings
from django.core.mail import send_mail
import datetime
import os,json

count=1

# 发往：/picSave
# 返回：/picSave/filename.
# 用来接收前端文本编辑发送上来的文件
class getPic(APIView):
    def post(self,request):
        myFile = request.FILES.get("image", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return Response("no files for upload!")
        destination = open(os.path.join(settings.MEDIA_ROOT, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()
        old_dir=os.path.join(settings.MEDIA_ROOT, myFile.name)
        new_dir=os.path.join(settings.MEDIA_ROOT, myFile.name + str(count).zfill(4)+ os.path.splitext(myFile)[1])
        os.rename(old_dir,new_dir)
        return Response({
                'info': '上传成功',
                'code': 200,
            }, status=200)