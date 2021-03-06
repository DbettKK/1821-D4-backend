# Generated by Django 3.1 on 2020-08-12 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_remove_teammember_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privilegeteam',
            name='file',
        ),
        migrations.RemoveField(
            model_name='privilegeteam',
            name='member',
        ),
        migrations.RemoveField(
            model_name='file',
            name='dif_privilege',
        ),
        migrations.RemoveField(
            model_name='file',
            name='dif_team_privilege',
        ),
        migrations.AddField(
            model_name='file',
            name='permission',
            field=models.IntegerField(choices=[(1, '只能查看'), (2, '可评论和查看'), (3, '可编辑、评论和查看'), (4, '所有权限包括分享')], default=4, verbose_name='权限'),
        ),
        migrations.AddField(
            model_name='file',
            name='team_permission',
            field=models.IntegerField(choices=[(1, '成员只能查看'), (2, '成员可评论和查看'), (3, '成员可编辑、评论和查看'), (4, '成员所有权限包括分享')], default=4, verbose_name='团队权限'),
        ),
        migrations.DeleteModel(
            name='PrivilegePri',
        ),
        migrations.DeleteModel(
            name='PrivilegeTeam',
        ),
    ]
