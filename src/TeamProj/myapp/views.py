from rest_framework.views import APIView, Response
from rest_framework import generics
from .models import User, UserToken
from .serializers import UserInfoSer
from random import Random
import hashlib
import time


def md5(user):
    """md5 加密token"""
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def chk_token(token):
    if token is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    u = UserToken.objects.filter(token=token)
    if len(u) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return u.get().user_id


def random_str(randomlength=8):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    retstr = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        retstr += chars[random.randint(0, length)]
    return retstr


class UserInfoList(generics.ListAPIView):
    """用户详情页视图"""
    queryset = User.objects.all()
    serializer_class = UserInfoSer  # id, name, email, phone_num


class Index(generics.ListAPIView):
    """假设是个主页"""
    serializer_class = UserInfoSer

    def get_queryset(self):
        if 'username' in self.request.COOKIES:
            return User.objects.filter(username=self.request.COOKIES.get('username'))
        else:
            return None


# 放后面防止循环导入发生冲突
from .view.user import UserRegister, UserLogin, GetBackPassword, TestEmail, \
    TestEmail2, random_str, WriteOff, UserAchieve
from .view.userinfo import UserChkOldPwd, UserInfo
from .view.userfile import BrowseFile, Favorites, CancelFavorite, \
    CreateFilePri, CreateFileTeam, GetBrowseFiles, GetFavorites, GetCreateFiles, GetFile, \
    RenameFile, DelBrowseFile

from .view.userteam import CreateTeam, JoinTeam, ExitTeam, ShareTeam, GetAllTeams, GetTeamFile, DismissTeam
from .view.comment import CommentFile, GetComments
from .view.userfiledelete import FileIsDelete, FileRealDelete, GetTrashFiles, RemoveAll
from .view.fileprivilege import SetPriviFile, ChangeTeamToPri, JudgePriviPri, \
    JudgePriviTeam, ChangePriToTeam, SetPriviFileTeam
from .view.pic import getPic
from .view.fileSave import FileSave
from .view.fileedit import EditFile, JudgeEdit, SaveEdit
from .view.message import GetMsg, SetAllRead, GetAllUnread, UnreadMsg, MsgRead, SetTypeRead, AcceptInvite
from .view.team import InviteToTeam, GetTeam, CheckCreator, BeFiredTeam, GetMembers
from .view.createfile import CustomizeFile, ModelFile, PreviewFile





