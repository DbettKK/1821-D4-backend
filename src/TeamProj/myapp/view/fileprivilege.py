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
        if not all([privilege, file_id]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
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
        if f.type != 'private':
            return Response({
                'info': '文档类型有误',
                'code': 403
            }, status=403)
        f.permission = pri
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class SetPriviFileTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.POST.get('file_id')
        team_id = request.POST.get('team_id')
        privilege = request.POST.get('privilege')
        pri = int(privilege)
        if not all([team_id, privilege, file_id]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        if pri < 1 or pri > 4:
            return Response({
                'info': '权限有误',
                'code': 403
            }, status=403)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if f.type != 'team':
            return Response({
                'info': '文档类型有误',
                'code': 403
            }, status=403)
        t = Team.objects.filter(pk=team_id)
        if t:
            f.team_permission = pri
            f.save()
            return Response({
                'info': 'success',
                'code': 200,
                'data': FileSer(f).data
            }, status=200)
        return Response({
            'info': '不存在该团队',
            'code': 403
        }, status=403)


class ChangePrivi(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        file_id = request.POST.get('file_id')
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if f.type == 'private':
            f.type = 'team'
        if f.type == 'team':
            f.type = 'private'
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class JudgePriviPri(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        file_id = request.GET.get('file_id')
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if f.creator.id == user_id:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {'pri': 4}
            }, status=200)
        else:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {'pri': f.permission}
            }, status=200)


class JudgePriviTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        file_id = request.GET.get('file_id')
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if f.type != 'team':
            return Response({
                'info': '非团队文档',
                'code': 403,
            }, status=403)
        if f.team_belong.creator.id == user_id:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {'pri': 4}
            }, status=200)
        if f.creator.id == user_id:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {'pri': 4}
            }, status=200)
        else:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {'pri': f.permission}
            }, status=200)
