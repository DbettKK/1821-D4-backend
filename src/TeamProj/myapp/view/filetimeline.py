from django.utils import timezone
from django.db.models import Q
import json
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Message, Modify
from myapp.views import chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer, MsgSer, TeamMemberSer,ModifySer

def chk_file_id(file_id):
    try:
        f = File.objects.get(pk=file_id)
    except:
        return Response({
            'info': '文件不存在',
            'code': 403,
        }, status=403)
    return f

class GetFileTimeline(APIView):
    def get(self,request) :
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        if not all([file_id]):
            return Response({
                'info': '参数不完整',
                'code': 400,
                'registered': False,
            }, status=400)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        ret = Modify.objects.filter(file=f)
        return Response({
            'info': 'success',
            'code': 200,
            'data': ModifySer(ret, many=True).data
        }, status=200)
        