from django.urls import path, re_path
from . import views

app_name = 'myapp'
urlpatterns = [
    # 后端自用api
    path('', views.Index.as_view(), name='index'),
    path('userlist/', views.UserInfoList.as_view(), name='userList'),
    
    # 不需要token的api
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('email/', views.TestEmail.as_view(), name='email'),
    path('email2/', views.TestEmail2.as_view(), name='email2'),
    path('findpassword/', views.GetBackPassword.as_view(), name='get_back_password'),

    # 需要token的api   最好前面跟个子目录
    path('user/info/', views.UserInfo.as_view(), name='userinfo'),
    path('user/modify/', views.UserChkOldPwd.as_view()),
    path('user/writeoff/', views.WriteOff.as_view(), name='write_off'),
    path('user/achieve/', views.UserAchieve.as_view(), name='achievement'),

    path('file/browse/', views.BrowseFile.as_view(), name='browse_file'),

    path('file/browse/get/', views.GetBrowseFiles.as_view(), name='get_browse_files'),
    path('file/browse/delete/', views.DelBrowseFile.as_view(), name='del_browse_files'),
    path('file/isdelete/', views.FileIsDelete.as_view(), name='file_is_delete'),
    path('file/realdelete/', views.FileRealDelete.as_view(), name='file_real_delete'),
    path('file/delete/get/', views.GetTrashFiles.as_view(), name='get_delete_file'),
    path('file/delete/all/', views.RemoveAll.as_view(), name='remove_all_trash_file'),

    path('file/create/model/team/', views.ModelFileTeam.as_view(), name='create_model_file_team'),
    path('file/create/customize/team/', views.CustomizeFileTeam.as_view(), name='create_customize_file_team'),
    path('file/create/preview/', views.PreviewFile.as_view(), name='preview_model_file'),
    path('file/create/model/', views.ModelFile.as_view(), name='create_model_file'),
    path('file/create/customize/', views.CustomizeFile.as_view(), name='create_customize_file'),
    path('file/create/pri/', views.CreateFilePri.as_view(), name='create_pri_file'),
    path('file/create/team/', views.CreateFileTeam.as_view(), name='create_team_file'),
    path('file/team/get/', views.GetTeamFile.as_view(), name='get_team_file'),
    path('file/create/all/get/', views.GetCreateFiles.as_view(), name='get_create_file_all'),
    path('file/get/', views.GetFile.as_view(), name='get_file'),
    path('file/favorite/', views.Favorites.as_view(), name='favorite'),
    path('file/cancelfavor/', views.CancelFavorite.as_view(), name='cancel_favorite'),
    path('file/favorite/get/', views.GetFavorites.as_view(), name='get_favorites'),

    path('file/edit/save/', views.SaveEdit.as_view(), name='save_edit_file'),
    path('file/edit/judge/', views.JudgeEdit.as_view(), name='judge_edit_file'),
    path('file/edit/', views.EditFile.as_view(), name='edit_file'),
    path('team/create/', views.CreateTeam.as_view(), name='create_team'),
    path('team/join/<int:team_id>/', views.JoinTeam.as_view(), name='join_team'),
    path('team/exit/', views.ExitTeam.as_view(), name='exit_team'),
    path('team/share/', views.ShareTeam.as_view(), name='share_team'),
    path('team/all/get/', views.GetAllTeams.as_view(), name='get_create_team'),
    path('team/dismiss/', views.DismissTeam.as_view(), name='dismiss_team'),

    path('team/kickoff/', views.BeFiredTeam.as_view(), name='kickoff_team'),
    path('team/invite/', views.InviteToTeam.as_view(), name='invite_to_team'),
    path('team/check/creator/', views.CheckCreator.as_view(), name='check_team_creator'),
    path('team/get/', views.GetTeam.as_view(), name='get_team'),
    path('team/members/get/', views.GetMembers.as_view(), name='get_members'),
    path('team/accept/', views.AcceptInvite.as_view(), name='accept_invite'),
    path('team/refuse/', views.RefuseInvite.as_view(), name='refuse_invite'),

    path('file/privi/team/',views.SetPriviFileTeam.as_view(), name='set_privi_team'),
    path('file/privi/pri/',views.SetPriviFile.as_view(), name='set_privi_pri'),
    path('file/privi/change/pri/', views.ChangeTeamToPri.as_view(), name='change_file_privi'),
    path('file/privi/change/team/', views.ChangePriToTeam.as_view(), name='change_file_privi_to_team'),
    path('file/rename/',views.RenameFile.as_view(), name='set_privi_pri'),
    path('file/comment/', views.CommentFile.as_view(), name='comment'),
    path('file/comment/get/', views.GetComments.as_view(), name='get_comment'),

    path('agrees/get/', views.GetNum.as_view(), name='get_agrees'),
    path('comment/agree/', views.UserAgree.as_view(), name='agrees'),
    path('comment/disagree/', views.UserDisagree.as_view(), name='disagrees'),
    path('picSave/', views.getPic.as_view(), name='picSave'),
    path('mdSave/', views.FileSave.as_view(), name='mdSave'),

    path('private/privi/judge/', views.JudgePriviPri.as_view(), name='judge_pri_privi'),
    path('team/privi/judge/', views.JudgePriviTeam.as_view(), name='judge_team_privi'),

    path('getmsg/', views.GetMsg.as_view(), name='getmsg'),

    path('get/unread/counts/', views.GetAllUnread.as_view(), name='get_unread_msg'),
    path('set/type/read/all/', views.SetTypeRead.as_view(), name='set_type_msg_read'),
    path('set/read/all/', views.SetAllRead.as_view(), name='set_all_msg_read'),
    path('set/read/', views.MsgRead.as_view(), name='set_msg_read'),
    path('set/unread/', views.UnreadMsg.as_view(), name='set_msg_unread'),
    path('msg/delete/', views.DeleteMessage.as_view(), name='del_msg'),
    path('msg/delete/all/', views.DeleteType.as_view(), name='del_type_msg'),
    path('msg/sendInnerMessage/', views.ShareMessage.as_view(), name='share_massge'),
]