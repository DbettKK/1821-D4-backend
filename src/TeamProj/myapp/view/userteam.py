from rest_framework.views import APIView, Response
from django.db.models import Q
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, TeamMember, Message
from myapp.views import chk_token, avatar
from myapp.serializers import TeamMemberSer, TeamSer, FileSer


class CreateTeam(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        name = request.POST.get('team_name')
        if name is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        ava = avatar(name)
        t = Team.objects.create(
            creator=u,
            name=name,
            avatar=ava
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamSer(t).data
        }, status=200)


class JoinTeam(APIView):
    def get(self, request, team_id):
        token = request.META.get('HTTP_TOKEN')
        # team_id = request.GET.get('team_id')
        if team_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        if TeamMember.objects.filter(team=t, member=u):
            return Response({
                'info': '你已经加入该团队',
                'code': 403,
            }, status=403)
        tm = TeamMember.objects.create(team=t, member=u)
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamMemberSer(tm).data
        }, status=200)


class ExitTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        if team_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        tm = TeamMember.objects.filter(team=t, member=u)
        if t.creator.id == user_id:
            return Response({
                'info': '您是团队创建者，不能退出团队',
                'code': 403,
            }, status=403)
        if len(tm) <= 0:
            return Response({
                'info': '未加入该团队 无法退出',
                'code': 403,
            }, status=403)
        res = TeamMemberSer(tm.get()).data
        # t_id = tm.get().team.pk
        tm.get().delete()
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)


class ShareTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        if team_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        return Response({
            'info': 'success',
            'code': 200,
            'data': {
                'url': 'http://175.24.121.113:8000/myapp/team/join/' + team_id
            }
        }, status=200)


class GetAllTeams(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        teams = Team.objects.filter(Q(creator=u) | Q(members__pk=user_id)).distinct().order_by('id')
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamSer(teams, many=True).data
        }, status=200)


class GetTeamFile(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        tfiles = File.objects.filter(team_belong=t)
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(tfiles, many=True).data
        }, status=200)


class DismissTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.get(pk=team_id)
        if t.creator.id != user_id:
            return Response({
                'info': '你不能解散团队，只有创建者可以',
                'code': 403
            }, status=403)
        res = TeamSer(t).data
        Team.objects.filter(pk=team_id).delete()

        for single_member in t.members.all():
            Message.objects.create(
                user=single_member,
                msg_type='team',
                msg_title='团队解散',
                msg_content='团队 ' + t.name + '\'s ' + '被 ' + u.username + ' 解散',
                msg_type_from=t.id,
                msg_person_from=user_id,
                msg_type_from_name=t.name,
                msg_person_from_name=u.username
            )
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)

