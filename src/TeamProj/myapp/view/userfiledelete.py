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

#回收站api，添加或恢复
class FileIsDelete(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        is_delete = request.GET.get('is_delete')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if f:
            if is_delete == False:
                f.is_delete = False
                f.save()
            else:
                f.is_delete = True
                f.save()
        else:
            return Response({
                'info': 'not_found_file',
                'code': 403,
            }, status=403)
        return Response({
            'info': 'success',
            'code': 200,
        }, status=200)

#在回收站中彻底删除
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
        if f:
            f.delete()
            return Response({
                'info': 'success',
                'code': 200,
            }, status=200)
        else:
            return Response({
                'info': 'not_found_file',
                'code': 403,
            }, status=403)
