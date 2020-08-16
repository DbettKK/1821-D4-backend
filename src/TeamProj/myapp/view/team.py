from myapp.models import Modify, File, User, Team, Message
from myapp.serializers import FileSer, MsgSer, TeamSer
from myapp.views import chk_token
from .userfile import chk_file_id
from rest_framework.views import APIView, Response


class InviteToTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.POST.get('team_id')
        member_name = request.POST.get('member_name')
        member_id = request.POST.get('member_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        if len(t.members.filter(pk=user_id)) <= 0 and t.creator.id != user_id:
            return Response({
                'info': '非团队成员不能邀请进入团队',
                'code': 403,
            }, status=403)
        if member_name is None and member_id is None:
            return Response({
                'info': '请至少传递一个参数',
                'code': 400,
            }, status=400)
        if member_name is None:
            member = User.objects.get(pk=member_id)
        if member_id is None:
            member = User.objects.get(username=member_name)

        msg = Message.objects.create(
            user=member,
            msg_type='team',
            msg_title='TEAM BOOMING',
            msg_content='THE TEAM ' + t.name + '\'s ' + u.username + ' INVITE YOU TO JOIN THEM!',
            msg_from=t.name
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(msg).data
        }, status=400)


# 被踢出团队
class BeFiredTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.POST.get('team_id')
        member_name = request.POST.get('member_name')
        member_id = request.POST.get('member_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        if len(t.members.filter(pk=user_id)) <= 0 :
            return Response({
                'info': '已经不是团队成员',
                'code': 403,
            }, status=403)
        if t.creator.id != user_id:
            return Response({
                'info': '不是团队管理者',
                'code': 403
            },status=403)
        if member_name is None and member_id is None:
            return Response({
                'info': '请至少传递一个参数',
                'code': 400,
            }, status=400)
        if member_name is None:
            member = User.objects.get(pk=member_id)
        if member_id is None:
            member = User.objects.get(username=member_name)
        msg = Message.objects.create(
            user=member,
            msg_type='team',
            msg_title='TEAM LAYOFF',
            msg_content='THE TEAM ' + t.name + '\'s ' + ' YOU HAVE BE REMOVED FROM THE TEAM!',
            msg_from=t.name
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(msg).data
        }, status=400)


class CheckCreator(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        t = Team.objects.get(pk=team_id)
        if t.creator.id == user_id:
            return Response({
                'info': 'success',
                'code': 200,
                'data': {
                    'is_creator': True
                }
            }, status=200)
        return Response({
            'info': '不是创建者',
            'code': 403,
        }, status=403)


class GetTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        t = Team.objects.get(pk=team_id)
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamSer(t).data
        }, status=200)


