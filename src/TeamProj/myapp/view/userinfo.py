from rest_framework.views import APIView, Response
from django.contrib.auth.hashers import make_password
from myapp.models import User
from myapp.serializers import UserInfoSer
from myapp.views import chk_token


class UserChkOldPwd(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        old_pwd = request.POST.get('old_password')
        u = User.objects.get(pk=user_id)
        if u.check_pwd(old_pwd):
            return Response({
                'info': 'success',
                'code': 200,
                'data': UserInfoSer(u).data
            }, status=200)
        else:
            return Response({
                'info': '旧密码错误',
                'code': 403
            }, status=403)


class UserInfo(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        res = User.objects.get(pk=user_id)
        return Response({
            'info': 'success',
            'code': 200,
            'data': UserInfoSer(res).data
        }, status=200)

    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        print(token)
        user_id = chk_token(token)
        if isinstance(user_id, Response):
            return user_id
        pwd = request.POST.get('new_password')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        print(pwd)
        print(email)
        print(phone_num)
        if not all([pwd, email, phone_num]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        u = User.objects.get(pk=user_id)
        u.password = make_password(pwd)
        u.email = email
        u.phone_num = phone_num
        u.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': UserInfoSer(u).data
        }, status=200)
