from rest_framework import serializers
from .models import User, Comment, File, UserKeptFile, TeamMember, Team, UserBrowseFile, Message, Mod, Modify


class UserInfoSer(serializers.ModelSerializer):
    """用户详情信息序列化器"""
    myfiles = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = '__all__'


class CommentSer(serializers.ModelSerializer):
    username = serializers.CharField(source='person.username')
    agree_set = serializers.StringRelatedField(many=True)
    disagree_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = Comment
        fields = '__all__'


class FileSer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.username')

    class Meta:
        model = File
        fields = '__all__'


class UserKeptFileSer(serializers.ModelSerializer):
    file_creator_id = serializers.IntegerField(source='file.creator.id')
    file_privi = serializers.IntegerField(source='file.permission')
    file_name = serializers.CharField(source='file.file_title')
    file_creator_name = serializers.CharField(source='file.creator.username')
    person_name = serializers.CharField(source='person.username')
    file_isdelete = serializers.CharField(source='file.is_delete')

    class Meta:
        model = UserKeptFile
        fields = '__all__'


class UserBrowseFileSer(serializers.ModelSerializer):
    file_creator_id = serializers.IntegerField(source='file.creator.id')
    file_privi = serializers.IntegerField(source='file.permission')
    file_name = serializers.CharField(source='file.file_title')
    file_creator_name = serializers.CharField(source='file.creator.username')
    person_name = serializers.CharField(source='person.username')
    file_isdelete = serializers.CharField(source='file.is_delete')

    class Meta:
        model = UserBrowseFile
        fields = '__all__'


class TeamMemberSer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.username')
    member_email = serializers.CharField(source='member.email')
    member_phone_num = serializers.CharField(source='member.phone_num')
    member_create_time = serializers.CharField(source='member.create_time')
    class Meta:
        model = TeamMember
        fields = '__all__'


class TeamSer(serializers.ModelSerializer):
    teamfiles = serializers.StringRelatedField(many=True)
    creator_name = serializers.CharField(source='creator.username')
    class Meta:
        model = Team
        fields = '__all__'


class MsgSer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class ModSer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = '__all__'


class ModifySer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='person.username')
    class Meta:
        model = Modify
        fields = '__all__'