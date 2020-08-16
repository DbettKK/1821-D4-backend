from django.test import TestCase
from requests import post, get
from .models import User, File, Mod


# 注册测试
class UserMethodTest(TestCase):
    def test_register(self):
        """注册成功"""
        res = post('http://175.24.121.113:8000/myapp/register/',
             data={'username': 'lisi',
                   'password': '123',
                   'password2': '123',
                   'email': '12@12.12',
                   'phone_num': '12345678912'})
        print(str(res.content, encoding="gbk"))

    def test_login_success(self):
        """登录成功"""
        res = post('http://175.24.121.113:8000/myapp/login/',
                   data={'username': 'lisi',
                         'password': '123'})
        print(str(res.content, encoding="gbk"))


