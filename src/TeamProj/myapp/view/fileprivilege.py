from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Comment
from myapp.serializers import CommentSer
from myapp.views import chk_token
from .userfile import chk_file_id


class SetPriFile(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        member_id = request.POST.get('member_id')
        team_id = request.POST.get('team_id')
        privilege = request.POST.get('privilege')

        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)


class GetPrivilege(APIView):
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

