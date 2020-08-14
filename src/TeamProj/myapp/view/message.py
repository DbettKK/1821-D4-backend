from django.utils import timezone
import json
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile,Message
from myapp.views import chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer, MsgSer


class GetMsg(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_types = request.GET.get('msg_types')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        if msg_types != 'favor' and msg_types != 'comment' and msg_types != 'team':
            return Response({
                'info': '消息类型错误',
                'code': 401,
            }, status=200)
        else:
            ret_msg = Message.objects.filter(user=u, msg_type=msg_types)
            return Response({
                'info': 'success',
                'code': 200,
                'data': MsgSer(ret_msg, many=True).data
            }, status=200)

