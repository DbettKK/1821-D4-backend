from django.utils import timezone
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Message, Mod
from .userfile import chk_file_id, chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer


class CustomizeFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_title = request.POST.get('file_name')
        type = request.POST.get('file_type')
        permisson = request.POST.get('file_privilege')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = File.objects.create(
            file_title=file_title,
            file_content='',
            type=type,
            permission=permisson,
            creator=u
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class ModelFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_title = request.POST.get('file_name')
        mod = request.POST.get('model')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        # 这里通过模板获得file_content
        file_content = Mod.objects.get(mod_id=mod)
        f = File.objects.create(
            file_title=file_title,
            file_content=file_content,
            type='private',
            creator=u
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)
