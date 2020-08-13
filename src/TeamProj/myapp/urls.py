from django.urls import path
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
    path('file/browse/', views.BrowseFile.as_view(), name='browse_file'),

    path('file/browse/get/', views.GetBrowseFiles.as_view(), name='get_browse_files'),
    path('file/isdelete/', views.FileIsDelete.as_view(), name='file_is_delete'),
    path('file/realdelete/', views.FileRealDelete.as_view(), name='file_real_delete'),
    path('file/delete/get/', views.GetTrashFiles.as_view(), name='get_delete_file'),

    path('file/create/pri/', views.CreateFilePri.as_view(), name='create_pri_file'),
    path('file/create/team/', views.CreateFileTeam.as_view(), name='create_team_file'),
    path('file/create/all/get/', views.GetCreateFiles.as_view(), name='get_create_file_all'),
    path('file/favorite/', views.Favorites.as_view(), name='favorite'),
    path('file/cancelfavor/', views.CancelFavorite.as_view(), name='cancel_favorite'),
    path('file/favorite/get/', views.GetFavorites.as_view(), name='get_favorites'),

    path('team/create/', views.CreateTeam.as_view(), name='create_team'),
    path('team/join/<int:team_id>', views.JoinTeam.as_view(), name='join_team'),
    path('team/exit/', views.ExitTeam.as_view(), name='exit_team'),
    path('team/share/', views.ShareTeam.as_view(), name='share_team'),
    path('team/all/get/', views.GetAllTeams.as_view(), name='get_create_team'),

    path('file/privi/pri/',views.SetPriviFile.as_view(), name='set_privi_pri'),

    path('file/comment/', views.CommentFile.as_view(), name='comment'),
]