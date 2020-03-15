"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include

from django.urls import path
from partjob import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('index/', views.index, name="index"),
    path('user_register/', views.user_register, name="user_register"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_forget/', views.user_foget, name="user_forget"),
    path('user_reset/', views.user_reset, name="user_reset"),
    path('user_check_name/',views.user_check_name, name='user_check_name'),
    path('user_check_mobile/', views.user_check_mobile, name='user_check_mobile'),
    path('user_check_pwd/', views.user_check_pwd, name='user_check_pwd'),
    path('user_check_email/', views.user_check_email, name='user_check_email'),
    path('user_send_mail/', views.user_send_mail, name='user_send_mail'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('zjz/', views.zjz, name='zjz'),
    path('jz/', views.jz, name='jz'),
    path('get_son_comment/', views.get_son_comment, name='get_son_comment'),
    path('comment_subject/', views.comment_subject, name='comment_subject'),
    path('shenqing_jz/', views.shenqing_jz, name='shenqing-jz'),
    path('jubao/', views.jubao, name='jubao'),
    path('sfhs/', views.sfhs, name='sfhs'),
    path('upload_img_z/', views.upload_img_z, name='upload_img_z'),
    path('upload_img_f/', views.upload_img_f, name='upload_img_f'),
    path('upload_img_y/', views.upload_img_y, name='upload_img_y'),
    path('upload_img_t/', views.upload_img_t, name='upload_img_t'),
    path('wyfb/', views.wyfb, name='wyfb'),
    path('grzl/', views.grzl, name='grzl'),
    path('wdfb/', views.wdfb, name='wdfb'),
    path('article_update/', views.article_update, name='article_update'),
    path('article_del/', views.article_del, name='article_del'),
    path('article_xiajia/', views.article_xiajia, name='article_xiajia'),
    path('usertojob/', views.usertojob, name='usertojob'),
    path('xxzx/', views.xxzx, name='xxzx'),
    path('notice/', views.notice, name='notice'),
    path('lxwm/', views.lxwm, name='lxwm'),

    path('admin/', include(('myadmin.urls', 'myadmin'), namespace="myadmin")),
]
