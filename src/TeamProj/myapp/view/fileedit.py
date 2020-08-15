from django.utils import timezone
import json
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team
from myapp.views import chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer
from .userfile import chk_file_id


class EditFile(APIView):
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
        f.is_edit_now = True
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class JudgeEdit(APIView):
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
        if f.is_edit_now is True:
            return Response({
                'info': '有人正在编辑当前文档 暂时不能进入编辑页面哦 请稍等片刻',
                'code': 403,
            }, status=403)
        else:
            return Response({
                'info': '可以进入编辑页面',
                'code': 200,
            }, status=200)


class SaveEdit(APIView):
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
        if f.is_edit_now is True:
            f.is_edit_now = False
            f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)