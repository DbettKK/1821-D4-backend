from django.utils import timezone
import json
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Team, Message
from myapp.views import chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer


def chk_file_id(file_id):
    try:
        f = File.objects.get(pk=file_id)
    except:
        return Response({
            'info': '文件不存在',
            'code': 403,
        }, status=403)
    return f


class BrowseFile(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        print(token)
        print(file_id)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f

        ubf = UserBrowseFile.objects.update_or_create(person=u, file=f)[0]

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserBrowseFileSer(ubf).data
        }, status=200)


class GetBrowseFiles(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        now = timezone.now() + timezone.timedelta(days=-10)
        print(now)
        files = UserBrowseFile.objects.filter(person=u, last_modified__gte=now)
        print(files)

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserBrowseFileSer(files, many=True).data
        }, status=200)


class Favorites(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        print(token)
        print(file_id)

        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if len(UserKeptFile.objects.filter(person=u, file=f)) > 0:
            return Response({
                'info': '你已经收藏过该文档了',
                'code': 403,
            }, status=403)

        ukf = UserKeptFile.objects.update_or_create(person=u, file=f)[0]
        # 收藏的同时，创建类型为favor的消息,发送给文件的创建人
        Message.objects.create(
            user=f.creator,
            msg_type='favor',
            msg_title='文档收藏!',
            msg_content='你的文档 ' + f.file_title + ' 被 ' +
                        u.username + ' 收藏',
            msg_type_from=f.id,
            msg_person_from=user_id
        )

        print(ukf)
        return Response({
            'info': 'success',
            'code': 200,
            'data': UserKeptFileSer(ukf).data
        }, status=200)


class CancelFavorite(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        print(token)
        print(file_id)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        ukf = UserKeptFile.objects.filter(person=u, file=f)
        res = UserKeptFileSer(ukf.get()).data
        print(ukf)
        if len(ukf) > 0:
            # file_id = ukf.get().file_id
            ukf.get().delete()
            Message.objects.create(
                user=f.creator,
                msg_type='favor',
                msg_title='文档取消收藏',
                msg_content='你的文档 ' + f.file_title + ' 不再被 ' +
                            u.username + ' 收藏!',
                msg_type_from=f.id,
                msg_person_from=user_id
            )
            return Response({
                'info': 'success',
                'code': 200,
                'data': res
            }, status=200)

        return Response({
            'info': '你未收藏过该文档, 无法删除',
            'code': 403,
        }, status=403)


class GetFavorites(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        files = UserKeptFile.objects.filter(person=u)
        print(files)

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserKeptFileSer(files, many=True).data
        }, status=200)


class CreateFilePri(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = File.objects.create(
            file_content='',
            type='private',
            creator=u
        )

        # f = File.objects.filter(pk=f.pk).values()

        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class CreateFileTeam(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        t = Team.objects.filter(pk=team_id)
        if len(t) <= 0:
            return Response({
                'info': '团队不存在',
                'code': 403
            }, status=403)
        t = t.get()
        f = File.objects.create(
            file_content='',
            type='team',
            creator=u,
            team_belong=t
        )
        # f = File.objects.filter(pk=f.pk).values()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class GetCreateFiles(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        files = File.objects.filter(creator=u, is_delete=False)
        print(files)

        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(files, many=True).data
        }, status=200)


class RenameFile(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.POST.get('file_id')
        name = request.POST.get('file_name')
        print(name)
        print(file_id)
        if not all([name, file_id]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        f.file_title = name
        f.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': FileSer(f).data
        }, status=200)


class GetFile(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.GET.get('file_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        ukf = UserKeptFile.objects.filter(person=u, file=f)
        if ukf:
            is_kept = True
        else:
            is_kept = False
        if isinstance(f, Response):
            return f
        return Response({
            'info': 'success',
            'code': 200,
            'is_kept': is_kept,
            'data': FileSer(f).data
        }, status=200)


class DelBrowseFile(APIView):
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
        ubk = UserBrowseFile.objects.get(person=u, file=f)
        res = UserBrowseFileSer(ubk).data
        UserBrowseFile.objects.filter(person=u, file=f).delete()
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)



