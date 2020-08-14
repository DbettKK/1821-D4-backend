from myapp.models import Modify, File, User
from myapp.serializers import FileSer
from myapp.views import chk_token
from .userfile import chk_file_id
from rest_framework.views import APIView, Response


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
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        f.file_content = content
        f.file_title = title
        f.is_edit_now = False
        f.modified_times += 1
        Modify.objects.create(person=u, file=f)
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)