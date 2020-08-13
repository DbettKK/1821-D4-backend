from django.contrib.auth.hashers import make_password

from myapp.models import User, UserToken, EmailRecord,File
from myapp.serializers import FileSer
from myapp.views import md5, random_str,chk_token
from rest_framework.views import APIView, Response
from django.conf import settings
from django.core.mail import send_mail
import datetime

def chk_file_id(file_id):
    try:
        f = File.objects.get(pk=file_id)
    except:
        return Response({
            'info': '文件不存在',
            'code': 403,
        }, status=403)
    return f

class FileSave(APIView):
    """保存上传过来的md形式文档"""
    authentication_classes = []

    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not all([title,content,file_id]):
            return Response({
                'info': '参数不完整',
                'code': 400,
                'registered': False,
            }, status=400)

        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        f.content=content
        f.title=title
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)

        