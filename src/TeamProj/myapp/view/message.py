from django.utils import timezone
from django.db.models import Q
import json
from rest_framework.views import APIView, Response
from myapp.models import User, File, UserBrowseFile, UserKeptFile, Message, Team, TeamMember
from myapp.views import chk_token
from myapp.serializers import FileSer, UserKeptFileSer, UserBrowseFileSer, MsgSer, TeamMemberSer

def chk_file_id(file_id):
    try:
        f = File.objects.get(pk=file_id)
    except:
        return Response({
            'info': '文件不存在',
            'code': 403,
        }, status=403)
    return f

class GetMsg(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_types = request.GET.get('msg_types')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        if msg_types != 'favor' and msg_types != 'comment' and msg_types != 'team':
            return Response({
                'info': '消息类型错误',
                'code': 401,
            }, status=200)
        else:
            ret_msg = Message.objects.filter(user=u, msg_type=msg_types)
            return Response({
                'info': 'success',
                'code': 200,
                'data': MsgSer(ret_msg, many=True).data
            }, status=200)


class SetTypeRead(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_types = request.GET.get('msg_types')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        if msg_types != 'favor' and msg_types != 'comment' and msg_types != 'team':
            return Response({
                'info': '消息类型错误',
                'code': 401,
            }, status=200)
        msgs = Message.objects.filter(user=u, msg_type=msg_types)
        msgs.update(msg_is_read=True)
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(msgs, many=True).data
        }, status=200)


class SetAllRead(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        msgs = Message.objects.filter(user=u)
        msgs.update(msg_is_read=True)
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(msgs, many=True).data
        }, status=200)


class GetAllUnread(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        msgs = Message.objects.filter(user=u, msg_is_read=False).count()
        return Response({
            'info': 'success',
            'code': 200,
            'data': {
                'count': msgs
            }
        }, status=200)


class MsgRead(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_id = request.GET.get('msg_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        m = Message.objects.get(id=msg_id)
        if m.msg_is_read is True:
            return Response({
                'info': '该消息已经是已读状态了',
                'code': 403
            }, status=403)
        m.msg_is_read = True
        m.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(m).data
        }, status=200)


class UnreadMsg(APIView):
    """设为未读"""
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_id = request.GET.get('msg_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        m = Message.objects.get(id=msg_id)
        if m.msg_is_read is False:
            return Response({
                'info': '该消息已经是未读状态了',
                'code': 403
            }, status=403)
        m.msg_is_read = False
        m.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': MsgSer(m).data
        }, status=200)


class AcceptInvite(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_id = request.GET.get('msg_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        m = Message.objects.get(id=msg_id)
        u = User.objects.get(pk=user_id)
        if m.user_id == user_id and m.msg_type == 'team':
            tid = m.msg_type_from
            t = Team.objects.get(pk=tid)
            if TeamMember.objects.filter(team=t, member=u) or t.creator.id == user_id:
                return Response({
                    'info': '你已经加入过该团队了',
                    'code': 403
                }, status=403)
            tm = TeamMember.objects.create(team=t, member=u)
            rm = Message.objects.create(
                user=t.creator,
                msg_type='team',
                msg_title='新团队成员',
                msg_content='用户 ' + u.username + ' 加入了你的团队 ' + t.name + ' ',
                msg_type_from=t.id,
                msg_person_from=user_id,
                msg_type_from_name=t.name,
                msg_person_from_name=u.username
            )
            m.msg_is_accept=True
            m.save()
            return Response({
                'info': 'success',
                'code': 200,
                'data': MsgSer(rm).data
            }, status=200)
        return Response({
            'info': '无效接受',
            'code': 403
        }, status=403)


class RefuseInvite(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_id = request.GET.get('msg_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        m = Message.objects.get(id=msg_id)
        u = User.objects.get(pk=user_id)
        if m.user_id == user_id and m.msg_type == 'team':
            tid = m.msg_type_from
            t = Team.objects.get(pk=tid)
            rm = Message.objects.create(
                user=User.objects.get(pk=m.msg_person_from),
                msg_type='team',
                msg_title='团队邀请被拒绝',
                msg_content='用户 ' + u.username + ' 拒绝加入您的团队 ' + t.name,
                msg_type_from=t.id,
                msg_person_from=user_id,
                msg_type_from_name=t.name,
                msg_person_from_name=u.username
            )
            m.msg_is_accept = False
            m.save()
            return Response({
                'info': 'success',
                'code': 200,
                'data': MsgSer(rm).data
            }, status=200)
        return Response({
            'info': '无效拒绝',
            'code': 403
        }, status=403)


class DeleteMessage(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_id = request.GET.get('msg_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        m = Message.objects.get(id=msg_id)
        res = MsgSer(m).data
        u = User.objects.get(pk=user_id)
        Message.objects.filter(id=msg_id).delete()
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)


class DeleteType(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        msg_type = request.GET.get('msg_type')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        Message.objects.filter(user=u, msg_type=msg_type).delete()
        return Response({
            'info': 'success',
            'code': 200
        }, status=200)

#获取站内的分享消息
class ShareMessage(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        file_id = request.POST.get('file_id')
        messageTo = request.POST.get('shareMessageTo')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        f = chk_file_id(file_id)
        if isinstance(f, Response):
            return f
        if User.objects.filter(Q(username=messageTo) | Q(email=messageTo)):
            m=Message.objects.create(
                user=User.objects.get(Q(username=messageTo) | Q(email=messageTo)),
                msg_type = 'share',
                msg_title = '分享文件',
                msg_content = 'http://175.24.121.113/edit/'+file_id,
                msg_type_from = f.id,
                msg_person_from = user_id,
                msg_type_from_name = f.file_title,
                msg_person_from_name = u.username
            )
        else:
            return Response({
            'info':'用户不存在',
            'code':403
            },status=403)
        return Response({
            'info': 'success',
            'code': 200,
        } , status=200)