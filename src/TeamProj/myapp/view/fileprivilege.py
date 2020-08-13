from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Comment
from myapp.serializers import CommentSer, FileSer
from myapp.views import chk_token
from .userfile import chk_file_id


class SetPriviFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.POST.get('file_id')
        privilege = request.POST.get('privilege')
        # 判断是否是私人文档
        pri = int(privilege)
        if pri < 1 or pri > 4:
            return Response({
                'info': '权限有误',
                'code': 403
            }, status=403)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        # u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        f.permission = pri
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)





class GetPrivilege(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f

