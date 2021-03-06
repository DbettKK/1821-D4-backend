from django.utils import timezone
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Message, Mod
from .userfile import chk_file_id, chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer, ModSer


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
        file_content = Mod.objects.get(mod_id=mod).mod_content
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


class PreviewFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        mod = request.POST.get('model')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        # 这里通过模板获得file_content
        m = Mod.objects.get(mod_id=mod)
        return Response({
            'info': 'success',
            'code': 200,
            'data': ModSer(m).data
        }, status=200)


class OtherPreviewFile(APIView):
    def get(self, request):
        file_id = request.GET.get('file_id')
        f = File.objects.get(pk=file_id)
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)



class CustomizeFileTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_title = request.POST.get('file_name')
        team_id = request.POST.get('team_id')
        permission = request.POST.get('file_privilege')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        f = File.objects.create(
            file_title=file_title,
            file_content='',
            type='team',
            team_permission=permission,
            creator=u,
            team_belong=t
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class ModelFileTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_title = request.POST.get('file_name')
        mod = request.POST.get('model')
        team_id = request.POST.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        # 这里通过模板获得file_content
        file_content = Mod.objects.get(mod_id=mod).mod_content
        f = File.objects.create(
            file_title=file_title,
            file_content=file_content,
            type='team',
            creator=u,
            team_belong=t
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)