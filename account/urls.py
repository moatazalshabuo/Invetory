from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('setting/',setting,name="setting"),
    path('email-setting',email,name="email.setting"),
    path('login/', view_login, name='login'),
    path('logout/', view_logout, name='logout'),
    path("users/",users,name='users'),
    path('users/create/',create_user,name="users.create"),
    path('usrs/change-status/<int:id>/',change_status,name="users.change.status"),
    path('users/edit/<int:id>/',update_user,name='users.edit'),
    path("<int:id>/password/", change_password, name="change.pass"),
    path("<int:id>/set-password/", set_password, name="set.pass"),
    path("assing_permisson/<int:id>/",assing_permission,name="assing.permission"),
    path('email/<int:id>/delete',delete_email,name='email.delete'),
]