from myapp.models import Modify, File, User, Team, Message, TeamMember
from myapp.serializers import FileSer, MsgSer, TeamSer, TeamMemberSer
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
        if len(t.members.filter(pk=user_id)) <= 0 or t.creator.id != user_id:
            return Response({
                'info': '非团队成员不能邀请别人进入团队',
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
            msg_title='团队邀请',
            msg_content= u.username + ' 邀请你加入他的团队 '+ t.name,
            msg_type_from=t.id,
            msg_person_from=user_id
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
        if len(TeamMember.objects.filter(team=t, member=member)) <= 0:
            return Response({
                'info': '不是团队成员',
                'code': 403,
            }, status=403)
        TeamMember.objects.filter(team=t, member=member).delete()
        msg = Message.objects.create(
            user=member,
            msg_type='team',
            msg_title='被踢出团队',
            msg_content= '你从团队 ' + t.name + '中被移出',
            msg_type_from=t.id,
            msg_person_from=user_id
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(msg).data
        }, status=200)


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


class GetMembers(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        t = Team.objects.get(pk=team_id)
        tms = TeamMember.objects.filter(team=t)
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamMemberSer(tms, many=True).data
        }, status=200)


