from rest_framework import serializers
from .models import User, Comment, File, UserKeptFile, TeamMember, Team, UserBrowseFile


# class CreateUserSer(serializers.ModelSerializer):
#     """新增用户序列化器"""
#     password2 = serializers.CharField(max_length=128, write_only=True)
#
#     def validate(self, attrs):
#         password = attrs['password']
#         password2 = attrs['password2']
#         if password != password2:
#             raise serializers.ValidationError('两次密码不一致，请重新输入！')
#         return attrs
#
#     def create(self, validated_data):
#         del validated_data['password2']
#         user = super().create(validated_data)
#         user.set_pwd(validated_data['password'])
#         user.save()
#         return user
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'phone_num')


class UserInfoSer(serializers.ModelSerializer):
    """用户详情信息序列化器"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_num')


class CommentSer(serializers.ModelSerializer):
    username = serializers.CharField(source='person.username')

    class Meta:
        model = Comment
        fields = '__all__'


class FileSer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class UserKeptFileSer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='file.file_title')
    file_creator_name = serializers.CharField(source='file.creator.username')
    person_name = serializers.CharField(source='person.username')

    class Meta:
        model = UserKeptFile
        fields = '__all__'


class UserBrowseFileSer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='file.file_title')
    file_creator_name = serializers.CharField(source='file.creator.username')
    person_name = serializers.CharField(source='person.username')

    class Meta:
        model = UserBrowseFile
        fields = '__all__'


class TeamMemberSer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class TeamSer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'