from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, TeamMember
from myapp.views import chk_token
from myapp.serializers import TeamMemberSer, TeamSer


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
        t = Team.objects.create(
            creator=u,
            name=name
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
        teams = Team.objects.filter(creator=u)
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamSer(teams, many=True).data
        }, status=200)




