from myapp.models import Modify, File, User, Team, Message
from myapp.serializers import FileSer, MsgSer
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
