from django.contrib.auth.hashers import make_password
from myapp.models import User, UserToken, EmailRecord, File, Team, UserBrowseFile, \
    UserKeptFile, TeamMember, Comment, Agree, Disagree
from myapp.serializers import UserInfoSer, TeamSer
from myapp.views import md5, random_str, chk_token, avatar
from rest_framework.views import APIView, Response
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import datetime


class UserLogin(APIView):
    '用户登录视图类'
    authentication_classes = []

    # 登录不需要认证

    def post(self, request):
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        print(username)
        print(pwd)

        if not all([username, pwd]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        try:
            user = User.objects.get(username=username)
        except:
            return Response({
                'info': '用户名不存在',
                'code': 403
            }, status=403)
        if user.check_pwd(pwd):
            # 登录成功后生成token
            token = md5(username)
            UserToken.objects.update_or_create(user=user, defaults={'token': token})
            res = {'info': 'success', 'token': token, 'code': 200, 'data': UserInfoSer(user).data}
            return Response(res)
        else:
            return Response({
                'info': '密码错误',
                'code': 403
            }, status=403)


class UserRegister(APIView):
    """用户注册视图"""
    authentication_classes = []

    def post(self, request):
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        code = request.POST.get('code')
        if not all([username, pwd, pwd2, email, phone_num, code]):
            return Response({
                'info': '参数不完整',
                'code': 400,
                'registered': False,
            }, status=400)
        if User.objects.filter(email=email):
            return Response({
                'info': 'emailExist',
                'code': 403,
                'registered': False,
            }, status=403)
        if User.objects.filter(username=username):
            return Response({
                'info': 'usernameExist',
                'code': 403,
                'registered': False,
            }, status=403)

        ava = avatar(email)
        current_time = datetime.datetime.now()
        if EmailRecord.objects.filter(email=email, code=code, exprie_time__gte=current_time, send_choice='register'):
            u = User.objects.create(
                username=username,
                password=make_password(pwd),
                email=email,
                phone_num=phone_num,
                isActive=True,
                avatar=ava
            )
            token = md5(username)
            user = User.objects.get(username=username)
            UserToken.objects.create(user=user, token=token)
            res = {'info': 'success', 'token': token, 'registered': True, 'code': 200, 'data': UserInfoSer(u).data}
            return Response(res)
        else:
            return Response({
                'info': '验证码过期',
                'code': 403,
                'registered': False,
            }, status=403)


class GetBackPassword(APIView):
    """找回密码类"""
    authentication_classes = []

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd_new = request.POST.get('password_new')
        code = request.POST.get('code')
        if not all([username, pwd_new]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        current_time = datetime.datetime.now()
        if EmailRecord.objects.filter(email=email, code=code, exprie_time__gte=current_time, send_choice='findpassword'):
            user = User.objects.filter(username=username)
            if user:
                user = user.get()
                user.password = make_password(pwd_new)
                user.save()
                return Response({
                    'info': '修改成功',
                    'code': 200
                }, status=200)
            return Response({
                'info': '用户不存在',
                'code': 403
            }, status=403)
        else:
            return Response({
                'info': '验证码错误',
                'code': 403
            }, status=403)


class TestEmail2(APIView):
    """找回密码的邮箱api"""
    authentication_classes = []

    def post(self, request):
        # 生成随机数码
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            return Response({
                'info': '该邮箱已注册',
                'code': 403,
                'emailed': False
            }, status=403)
        code = random_str(16)
        # 主题
        subject = '金刚石文档欢迎注册'
        # message表示发送的纯文本，
        # 如果需要发送带样式的，则使用html_message
        # 用html_message时，message为空字符串
        message = ''
        # 收件人列表
        receiver = [request.POST.get('email')]
        # 需要发送的带样式内容
        html_message = '<h1>金刚石文档提醒：您在修改账号密码</h1>' \
                       '您本次修改的验证码为：{0},验证码将在5分钟后失效<br>'.format(code)
        sender = settings.EMAIL_FROM
        # 　发送邮件
        send_result = send_mail(subject, message, sender, receiver, html_message=html_message)
        time_delta = datetime.datetime.now() + datetime.timedelta(minutes=5)
        email_record = EmailRecord.objects.create(email=email, code=code, exprie_time=time_delta,
                                                  send_choice='findpassword')
        if send_result == 1:
            return Response({
                'info': True,
                'code': 200,
                'emailed': True
            })
        else:
            return Response({
                'info': False,
                'code': 400,
                'emailed': False
            })


class TestEmail(APIView):
    """注册的邮箱api"""
    authentication_classes = []

    def post(self, request):
        # 生成随机数码
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            return Response({
                'info': '该邮箱已注册',
                'code': 403,
                'emailed': False
            }, status=403)
        code = random_str(16)
        # 主题
        subject = '金刚石文档欢迎注册'
        # message表示发送的纯文本，
        # 如果需要发送带样式的，则使用html_message
        # 用html_message时，message为空字符串
        message = ''
        # 收件人列表
        receiver = [request.POST.get('email')]
        # 需要发送的带样式内容
        html_message = '<h1>欢迎注册金刚石文档账号</h1>您本次注册的验证码为：{0},验证码将在5分钟后失效<br>'.format(code) 
            # 发送者
        sender = settings.EMAIL_FROM
        # 　发送邮件
        send_result = send_mail(subject, message, sender, receiver, html_message=html_message)
        time_delta = datetime.datetime.now() + datetime.timedelta(minutes=5)
        email_record = EmailRecord.objects.create(email=email, code=code, exprie_time=time_delta,
                                                  send_choice='register')
        if (send_result == 1):
            return Response({
                'info': True,
                'code': 200,
                'emailed': True
            })
        else:
            return Response({
                'info': False,
                'code': 400,
                'emailed': False
            })


class WriteOff(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)
        res = UserInfoSer(u).data
        User.objects.filter(pk=user_id).delete()
        # u.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': res
        }, status=200)


class UserAchieve(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        files = File.objects.filter(creator=u)
        files_delete = files.filter(is_delete=True).count()
        files_favor = UserKeptFile.objects.filter(person=u).count()
        files_been_favor = UserKeptFile.objects.filter(file__creator=u).count()
        comments = Comment.objects.filter(person=u)
        been_comment = Comment.objects.filter(file__creator=u).count()
        create_teams = Team.objects.filter(creator=u).count()
        join_teams = TeamMember.objects.filter(member=u).count()
        total_agree = 0
        total_disagree = 0
        for c in comments:
            total_agree += Agree.objects.filter(comment=c).count()
            total_disagree += Disagree.objects.filter(comment=c).count()
        return Response({
            'info': 'success',
            'code': 200,
            'data': {
                'username': u.username,
                'create_files': files.count(),
                'files_in_trash': files_delete,
                'files_favor': files_favor,
                'files_been_favor': files_been_favor,
                'make_comments': comments.count(),
                'receive_comments': been_comment,
                'create_teams': create_teams,
                'join_teams': join_teams,
                'total_agree': total_agree,
                'total_disagree': total_disagree
            }
        }, status=200)


class FinishInfo(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        addr = request.POST.get('address')
        age = request.POST.get('age')
        qq = request.POST.get('qq')
        gender = request.POST.get('gender')
        phone_num = request.POST.get('phone_num')
        if addr is not None:
            u.address = addr
        if age is not None:
            u.age = age
        if qq is not None:
            u.qq = qq
        if gender is not None:
            u.gender = gender
        if phone_num is not None:
            u.phone_num = phone_num
        u.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserInfoSer(u).data
        }, status=200)


class ChangeAvatar(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        u = User.objects.get(pk=user_id)

        ava = avatar(u.email + str(timezone.now()))
        u.avatar = ava
        u.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserInfoSer(u).data
        }, status=200)


class ChangeTeamAvatar(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        team_id = request.GET.get('team_id')
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        t = Team.objects.get(pk=team_id)

        ava = avatar(t.name + str(timezone.now()))
        t.avatar = ava
        t.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeamSer(t).data
        }, status=200)


class OtherInfo(APIView):
    def get(self, request):
        id = request.GET.get('id')
        name = request.GET.get('name')
        email = request.GET.get('email')
        if id is not None:
            u = User.objects.get(pk=id)
        if name is not None:
            u = User.objects.get(username=name)
        if email is not None:
            u = User.objects.get(email=email)

        return Response({
            'info': 'success',
            'code': 200,
            'data': UserInfoSer(u).data
        }, status=200)
