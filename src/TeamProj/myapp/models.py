from _datetime import datetime

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """
    用户类
    """
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    phone_num = models.CharField(max_length=11, verbose_name='电话')
    email = models.EmailField(unique=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')
    isActive = models.BooleanField(default=False)

    browse = models.ManyToManyField(
        'File',
        through='UserBrowseFile',
        through_fields=('person', 'file'),
        verbose_name='最近浏览',
        related_name='browse'
    )

    kept = models.ManyToManyField(
        'File',
        through='UserKeptFile',
        through_fields=('person', 'file'),
        verbose_name='收藏',
        related_name='kept'
    )

    def __str__(self):
        return self.username

    def set_pwd(self, password):
        self.password = make_password(password)
        return None

    def check_pwd(self, password):
        return check_password(password, self.password)


class UserToken(models.Model):
    """用户token表"""
    user = models.OneToOneField('User', on_delete=models.CASCADE)  # 与用户一对一关系
    token = models.CharField(max_length=64, verbose_name='token')


class EmailRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name='验证码')
    # 用户邮箱
    email = models.EmailField(max_length=50, verbose_name='用户邮箱')
    # 发送类型
    send_choice = models.CharField(max_length=20, verbose_name='发送类型')
    # 发送时间
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间', null=True, blank=True)
    # 过期时间
    exprie_time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'emailrecord'
        verbose_name_plural = verbose_name


# 标题、内容、文档基础信息、创建时间、修改时间、权限、作者信息(和user一对多)、评论(和user多对多)、分享连接(可通过id)
class File(models.Model):
    """文档类"""
    permissions = (
        (1, '只能查看'), (2, '可评论和查看'), (3, '可编辑、评论和查看'), (4, '所有权限包括分享')
    )
    team_permissions = (
        (1, '成员只能查看'), (2, '成员可评论和查看'), (3, '成员可编辑、评论和查看'), (4, '成员所有权限包括分享')
    )
    types = (('team', '团队文档'), ('private', '私人文档'))
    # file_name = models.CharField(max_length=64, verbose_name='文档名')
    file_title = models.CharField(max_length=64, verbose_name='文档标题', default='无标题')
    file_content = models.TextField(verbose_name='文档内容', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='文档创建时间')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='文档最后一次修改时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否在回收站')
    delete_time = models.DateTimeField(null=True, verbose_name='删除时间')
    is_edit_now = models.BooleanField(default=False, verbose_name='是否正在被编辑')

    modified_times = models.IntegerField(default=0, verbose_name='修改次数', null=True)
    modified_user = models.ManyToManyField(
        'User',
        through='Modify',
        through_fields=('file', 'person'),
        verbose_name='文档修改人',
        related_name='modified_name'
    )
    type = models.CharField(max_length=32, choices=types, verbose_name='文档类型')

    permission = models.IntegerField(choices=permissions, verbose_name='权限', default=4)

    team_permission = models.IntegerField(choices=team_permissions, verbose_name='团队权限', default=4)

    creator = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='myfiles',
        verbose_name='文档创建者'
    )
    comments = models.ManyToManyField(
        'User',
        through='Comment',
        related_name='comment_file',
        through_fields=('file', 'person'),
        verbose_name='评论',
    )
    team_belong = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='teamfiles',
        verbose_name='所属团队',
        null=True,
        blank=True
    )

    share = models.CharField(max_length=64, verbose_name='分享', null=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.file_title


class Comment(models.Model):
    person = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='评论人'
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.CASCADE,
        verbose_name='被评论的文档'
    )
    content = models.CharField(max_length=128, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论创建时间')

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.person.username + '评论' + self.file.file_title


class Team(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='team_own', verbose_name='团队创建者')
    members = models.ManyToManyField(
        'User',
        through='TeamMember',
        through_fields=('team', 'member'),
        verbose_name='团队成员',
    )
    name = models.CharField(max_length=32, verbose_name='团队名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='所属团队')
    member = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='团队成员')
    join_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    class Meta:
        ordering = ['-join_time']

    def __str__(self):
        return self.member.username + '加入' + self.team.name


class UserBrowseFile(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='浏览的文档')
    person = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='浏览的用户')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='最近一次浏览时间')

    class Meta:
        ordering = ['-last_modified']

    def __str__(self):
        return self.person.username + '浏览' + self.file.file_title


class UserKeptFile(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='收藏的文档')
    person = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='收藏的用户')
    kept_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        ordering = ['-kept_time']

    def __str__(self):
        return self.person.username + '收藏' + self.file.file_title


class Modify(models.Model):
    file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='被修改的文档')
    person = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='修改的用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    modify_times = models.IntegerField(default=0, verbose_name='修改次数')

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.person.username + '修改' + self.file.file_title


# class PrivilegePri(models.Model):
#     permissions = (
#         (1, '只能查看'), (2, '可评论和查看'), (3, '可编辑、评论和查看'), (4, '所有权限包括分享')
#     )
#
#     file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='文档')
#     person = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
#     permission = models.IntegerField(choices=permissions, verbose_name='权限')
#     modified_time = models.DateTimeField(auto_now=True, verbose_name='权限修改时间')
#
#     def __str__(self):
#         return self.person.username + '对' + self.file.file_title + '的权限'
#
#
# class PrivilegeTeam(models.Model):
#     team_permissions = (
#         (1, '只能查看'), (2, '可评论和查看'), (3, '可编辑、评论和查看'), (4, '所有权限包括分享')
#     )
#
#     file = models.ForeignKey('File', on_delete=models.CASCADE, verbose_name='文档')
#     member = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='成员')
#     team_permission = models.IntegerField(choices=team_permissions, verbose_name='团队权限')
#     modified_time = models.DateTimeField(auto_now=True, verbose_name='权限修改时间')
#
#     def __str__(self):
#         return self.member.username + '对' + self.file.file_title + '的权限'


class Message(models.Model):
    msg_types = (
        ('favor', '收藏'), ('comment', '评论'), ('team', '团队')
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='my_msg', verbose_name='用户')
    msg_type = models.CharField(max_length=32, choices=msg_types, verbose_name='消息类型')
    msg_title = models.CharField(max_length=128, verbose_name='消息头')
    msg_content = models.TextField(verbose_name='消息内容')
    msg_type_from = models.IntegerField(null=True, verbose_name='文件或团队id')
    msg_person_from = models.IntegerField(null=True, verbose_name='谁导致的这条消息')
    msg_time = models.DateTimeField(auto_now_add=True, verbose_name='消息时间')
    msg_is_read = models.BooleanField(default=False, verbose_name='消息是否已读')


class Mod(models.Model):
    mod_id = models.IntegerField(unique=True, verbose_name='模板唯一标识')
    mod_content = models.TextField(verbose_name='模板内容')

