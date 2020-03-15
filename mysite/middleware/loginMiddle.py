from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from partjob import models
from django.shortcuts import HttpResponse, redirect, render
import json
from datetime import datetime

class AuthMD(MiddlewareMixin):

    AJAX_REQUEST = [
        "/admin/ajax_user/",
        "/admin/ajax_article/",
        "/admin/del_article/",
        "/admin/del_user/",
        "/admin/show_xinyong/",
        "/admin/article_shenhe/",
        "/admin/shenhe_ajax/",
        "/admin/weigui/",
        "/admin/article_shenhe/",
        "/admin/update_wages/",
        "/admin/update_worktp/",
        "/admin/del_wages/",
        "/admin/del_worktp/",
        "/admin/user_shenhe/",
        "/admin/weigui/",
        "/admin/ajax_notice/",
        "/admin/del_notice/",
    ]

    ADMIN_URL = [
        '/admin/ajax_user/',
        '/admin/ajax_article/',
        '/admin/all_user/',
        '/admin/add_user/',
        '/admin/del_user/',
        '/admin/user_input/',
        '/admin/show_xinyong/',
        '/admin/add_xinyong/',
        '/admin/user_shenhe/',
        '/admin/shenhe_input/',
        '/admin/all_article/',
        '/admin/article_input/',
        '/admin/update_article/',
        '/admin/del_article/',
        '/admin/article_shenhe/',
        '/admin/find_shenhe/',
        '/admin/add_wages/',
        '/admin/add_worktp/',
        '/admin/shenhe_ajax/',
        '/admin/tags/',
        '/admin/update_wages/',
        '/admin/update_wages1/',
        '/admin/update_worktp/',
        '/admin/update_worktp1/',
        '/admin/del_wages/',
        '/admin/del_worktp/',
        '/admin/weigui/',
        '/admin/find_report/',
        '/admin/manager/',
        '/admin/manage_money/',
        '/admin/add_notice/',
        '/admin/login/',
        '/admin/notice/',
    ]

    USER_PAGE_NOT_NEED = [
        '/index/',
        '/user_login/',
        '/user_register/',
        '/user_forget/'
        '/user_check_name/',
        '/user_check_mobile/',
        '/user_check_pwd/',
        '/user_check_email/',
        '/user_send_mail/',
        '/notice/',
    ]

    USER_PAGE_NEED = [
        '/user_reset/',
        '/user_logout/',
        '/jz/',
        '/get_son_comment/',
        '/comment_subject/',
        '/shenqing_jz/',
        '/jubao/',
        '/zjz/',
        '/sfhs/',
        '/upload_img_z/',
        '/upload_img_f/',
        '/upload_img_y/',
        '/upload_img_t/',
        '/wyfb/',
        '/grzl/',
        '/wdfb/',
        '/article_update/',
        '/article_del/',
        '/article_xiajia/',
        '/usertojob/',
        '/xxzx/',
    ]

    def process_request(self,request):
        next_url = request.path
        admin_id = request.session.get("admin_id")
        user_id = request.session.get("user_id")

        if next_url in self.USER_PAGE_NOT_NEED:
            pass

        elif next_url in self.USER_PAGE_NEED:
            if request.method == "GET":
                if user_id:
                    try:
                        user = models.User.objects.get(id=user_id)
                        models.User.objects.filter(id=user_id).update(lastlogin_date=datetime.now())
                        request.u = user
                    except:
                        return redirect(reverse('user_login'))
                else:
                    return redirect(reverse('user_login'))

            elif request.method == "POST":
                if user_id:
                    try:
                        user = models.User.objects.get(id=user_id)
                        models.User.objects.filter(id=user_id).update(lastlogin_date=datetime.now())
                        request.u = user
                    except:
                        data = {
                            "status": 302,
                            "msg": "must login"
                        }
                        return HttpResponse(json.dumps(data))
                else:
                    data = {
                        "status": 302,
                        "msg": "must login"
                    }
                    return HttpResponse(json.dumps(data))


        if len(next_url) >= 6  and next_url[0:6] == "/admin":

            if next_url in self.AJAX_REQUEST and request.method == "POST":

                if admin_id:
                    try:
                        admin = models.Manages.objects.get(id = admin_id)
                        request.admin  = admin
                    except:
                        data={
                            "status" : 302,
                            "msg": "must login"
                        }
                        return HttpResponse(json.dumps(data))
                else:
                    data = {
                        "status": 302,
                        "msg": "must login"
                    }
                    return HttpResponse(json.dumps(data))

            elif next_url == "/admin/login/":
                pass

            else:
                if admin_id:
                    try:
                        admin = models.Manages.objects.get(id = admin_id)
                        request.admin  = admin
                    except:
                        return redirect(reverse("myadmin:admin_login"))
                else:
                    return redirect(reverse("myadmin:admin_login"))




