from django.utils import timezone
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team
from myapp.views import chk_token
from myapp.serializers import FileSer


def chk_file_id(file_id):
    try:
        f = File.objects.get(pk=file_id)
    except:
        return Response({
            'info': '文件不存在',
            'code': 403,
        }, status=403)
    return f


# 回收站api，添加或恢复
class FileIsDelete(APIView):
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
        if f.is_delete is True:
            f.is_delete = False
        else:
            f.is_delete = True
            f.delete_time = timezone.now()
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


# 在回收站中彻底删除
class FileRealDelete(APIView):
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
        res = FileSer(f).data
        f.delete()
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)


class GetTrashFiles(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        files = File.objects.filter(creator=u, is_delete=True)
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(files, many=True).data
        }, status=200)


class RemoveAll(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        files = File.objects.filter(creator=u, is_delete=True)
        res = FileSer(files, many=True).data
        File.objects.filter(creator=u, is_delete=True).delete()
        return Response({
            'info': 'success',
            'code': 200
        }, status=200)