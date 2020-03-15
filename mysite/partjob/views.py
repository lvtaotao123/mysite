from django.shortcuts import render
from utils.myform import *
from django.shortcuts import redirect,HttpResponse
from partjob.models import *
from django.http import JsonResponse
import re
from django.utils.safestring import mark_safe
import hashlib
import random
import os
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.core.cache import cache
from utils.func import *
from django.db.models import Q
from utils.page_list import PageArticle
import uuid
from mysite import settings
# Create your views here.
def index(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        if user_id:
            try:
                u = User.objects.get(id=user_id)
                request.u = u
            except:
                request.session.flush()
        notices = Notice.objects.filter(user_id = None).all()[0:9]

        zhaopins = Subject.objects.filter(xiajia=0, usertype=1,shenhe=1).order_by("-date").all()[0:28]
        zhaopin1 = zhaopins[0:9]
        zhaopin2 = zhaopins[9:18]
        zhaopin3 = zhaopins[18:27]
        qiuzhis = Subject.objects.filter(xiajia=0, usertype=2,shenhe=1).order_by("-date").all()[0:28]
        qiuzhi1 = qiuzhis[0:9]
        qiuzhi2 = qiuzhis[9:18]
        qiuzhi3 = qiuzhis[18:27]
        return render(request, 'index.html', locals())

def user_register(request):
    if request.method == "GET":
        user_form = User_form()
        return render(request, 'user_register.html', locals())
    elif request.method == "POST":
        form = User_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usertp = request.POST.get("usertp")
            if len(data["username"]) > 8 or len(data["username"]) < 4:
                return HttpResponse("<script>alert('昵称长度不对！');window.open('/user_register/' , target='_self');</script>")
            if cache.get(data["email"]) !=data["token"] :
                return HttpResponse("<script>alert('验证码输入错误！');window.open('/user_register/' , target='_self');</script>")
            if data["password"] != data['confirm_pwd']:
                return HttpResponse("<script>alert('两次密码不一致！');window.open('/user_register/' , target='_self');</script>")
            if data["token"] == cache.get(data["email"]) and data["password"] == data['confirm_pwd']:
                User.objects.create(username=data["username"], password=make_password(data["password"]), email=data["email"], tel = data["mobile"],usertype=usertp,sex=3,xinyong=100,idcardpath1='',idcardpath='',imagepath = '/static/pic/user_image.jpg')
                return HttpResponse("<script>alert('注册成功！');window.open('/user_login/' , target='_self');</script>")
            else:
                return HttpResponse("<script>alert('注册失败！');window.open('/user_register/' , target='_self');</script>")



def user_login(request):
    if request.method == "GET":
        return render(request, 'user_login.html')

    elif request.method == "POST":
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        u = User.objects.filter(Q(tel=user)|Q(email=user))
        if u.exists():
            us = u.first()
            if check_password(pwd, us.password):
                request.session["user_id"] = us.id
                return redirect(reverse("index"))
            else:
                return HttpResponse("<script>alert('密码错误！请重试！');window.open('/user_login/','_self');</script>")
        else:
            return HttpResponse("<script>alert('账号不存在');window.open('/user_login/','_self');</script>")
        return redirect(reverse("user_login"))

def user_foget(request):
    if request.method == "GET":
        return render(request, "user_forget.html")

    elif request.method == "POST":
        email = request.POST.get("email").lower()
        token = request.POST.get("token")
        new_pwd = request.POST.get("new_pwd")
        ret = re.match(r"^[0-9a-zA-Z-\._]+@([0-9a-zA-Z]+.)+[a-zA-Z0-9]+$", email)
        if not ret:
            return HttpResponse("<script>alert('邮箱格式错误！请重试！');window.open('/user_forget/','_self');</script>")
        elif len(new_pwd) > 16 or len(new_pwd) <6:
            return HttpResponse("<script>alert('密码不符合要求！');window.open('/user_forget/','_self');</script>")
        elif str(token) == str(cache.get(email)):
            User.objects.filter(email=email).update(password=make_password(new_pwd))

            return HttpResponse("<script>alert('密码设置成功！');window.open('/user_login/','_self');</script>")
        else:
            return HttpResponse("<script>alert('找回失败！');window.open('/user_forget/','_self');</script>")


def user_reset(request):
    if request.method == "GET":
        return render(request, "user_reset.html")

    elif request.method == "POST":
        user = request.user
        pwd = request.POST.get("pwd")
        new_pwd = request.POST.get("confirm_pwd")
        try:
            if check_password(pwd, user.password):
                if len(pwd) > 16 or len(pwd)<6:
                    return HttpResponse("<script>alert('新密码长度在6-16之间！');window.open('/user_reset/', '_self');</script>")
                u = User.objects.filter(id=user.id).update(password=make_password(new_pwd))
                request.session.flush()
                return HttpResponse("<script>alert('修改成功！请重新登录');window.open('/user_login/', '_self');</script>")
            else:
                return HttpResponse("<script>alert('原密码错误！');window.open('/user_reset/', '_self');</script>")
        except:
            return HttpResponse("<script>alert('修改失败检查您的错误！');window.open('/user_reset/', '_self');</script>")

def user_logout(request):
    if request.method == 'GET':
        request.session.flush()
        return redirect(reverse('index'))


def user_check_name(request):
    if request.method == "GET":
        username = request.GET.get("username")
        if len(username) > 8 or len(username) < 4:
            data={"status":300}
            return JsonResponse(data)
        if User.objects.filter(username=username).count():
            data={"status":300}
            return JsonResponse(data)
        else:
            data={"status":200}
            return JsonResponse(data)

def user_check_mobile(request):
    if request.method == "GET":
        mobile = request.GET.get("mobile")
        ret = re.match(r"^1[35678]\d{9}$", mobile)
        if not ret:
            data={"status":301}
            return JsonResponse(data)

        if User.objects.filter(tel=mobile).count():
            data={"status":300}
            return JsonResponse(data)
        else:
            data={"status":200}
            return JsonResponse(data)

def user_check_pwd(request):
    if request.method == "GET":
        pwd = request.GET.get("pwd")
        ret = re.match(r"[a-zA-Z0-9\._]{6,12}", pwd)
        if not ret:
            data={"status":300}
            return JsonResponse(data)
        else:
            data={"status":200}
            return JsonResponse(data)

def user_check_email(request):
    if request.method == "GET":
        email = request.GET.get("email").lower()
        ret = re.match(r"^[0-9a-zA-Z-\._]+@([0-9a-zA-Z]+.)+[a-zA-Z0-9]+$", email)

        if not ret:
            data={"status":301}
            return JsonResponse(data)

        if User.objects.filter(email=email).count():
            data={"status":300}
            return JsonResponse(data)
        else:
            data={"status":200}
            return JsonResponse(data)

def user_send_mail(request):
    email = request.GET.get("email")
    token = get_random_six()
    send_email(token, email)
    cache.set(email, token,  timeout=60 * 5)
    data = {"status":200}
    return JsonResponse(data)

def zjz(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        if user_id:
            try:
                u = User.objects.get(id=user_id)
                request.u = u
            except:
                request.session.flush()
        p = int(request.GET.get("p", 1))
        wages = int(request.GET.get('wages', 0))
        worktp = int(request.GET.get('worktp', 0))
        usertp = int(request.GET.get('usertp', 1))
        for_page_count = 10
        wages_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_wages"><option value="0" >全部</option>'
        worktp_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_worktp"><option value="0" >全部</option>'
        usertype_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_usertype">'
        if wages == 0 and worktp == 0:
            wages_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_wages"><option value="0" selected>全部</option>'
            worktp_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_worktp"><option value="0" selected>全部</option>'
            articless = Subject.objects.filter(shenhe=1, xiajia=0, usertype=usertp).order_by('-date')
        elif wages == 0 and worktp != 0:
            wages_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_wages"><option value="0" selected>全部</option>'
            articless = Subject.objects.filter(worktype=worktp, shenhe=1, xiajia=0, usertype=usertp).order_by('-date')
        elif wages != 0 and worktp == 0:
            worktp_select = '<select class="formccc" style="display: inline-block; font-size: 12px;  height:26px;border: 1px #eab67c solid;  border-radius: 3px;" id="select_worktp"><option value="0" selected>全部</option>'
            articless = Subject.objects.filter(wages=wages,shenhe=1, xiajia=0, usertype=usertp).order_by('-date')
        else:
            articless = Subject.objects.filter(wages=wages, worktype=worktp, shenhe=1, xiajia=0, usertype=usertp).order_by('-date')
        articles = articless[(p - 1) * for_page_count:p * for_page_count]
        data_count = len(articless)
        page = PageArticle(data_count, for_page_count, p, "/zjz")
        pagestr = page.page_list()
        w = Wages.objects.all()
        c = Captrue.objects.all()
        for i in w:
            if i.id == wages:
                wages_select += '<option value="{}" selected>{}</option>'.format(i.id, i.name)
            else:
                wages_select += '<option value="{}" >{}</option>'.format(i.id, i.name)
        wages_select += '</select>'
        for i in c:
            if i.id == worktp:
                worktp_select += '<option value="{}" selected>{}</option>'.format(i.id, i.name)
            else:
                worktp_select += '<option value="{}" >{}</option>'.format(i.id, i.name)
        if usertp == 1:
            usertype_select += '<option value="1" selected>招聘中心</option><option value="2">求职中心</option></select>'
        elif usertp == 2:
            usertype_select += '<option value="1" >招聘中心</option><option value="2" selected>求职中心</option></select>'
        worktp_select += '</select>'
        wages_select = mark_safe(wages_select)
        worktp_select = mark_safe(worktp_select)
        usertype_select = mark_safe(usertype_select)
        return render(request, 'zjz.html', locals())

def jz(request):
    if request.method == "GET":
        s_id = request.GET.get('id')
        try:
            article = Subject.objects.get(id=s_id)
        except:
            return redirect(reverse("zjz"))
        return render(request, 'jz.html', locals())

def get_son_comment(request):
    if request.method == "GET":
        pid= request.GET.get("pid")
        dic = build_comment(pid)
        html = ''
        for i in dic:
            username = i.userid.username
            date = i.date.strftime("%Y-%m-%d %H:%M")
            content = i.content
            if i.pid.id == None:
                html += '<div class="son-comment">'+username+':&nbsp;&nbsp;'+content+'<div style="maigin-top:2px;line-height: 16px;font-size:12px;color: #808080;">'+date+'<div style="width: 46px;float: right;cursor: pointer;"> <a class="a_huifu aa_huifu" style="cursor: pointer;">回复</a> </div></div><div class="huifu hide" ><textarea  style="width: 100%;height: 60px;margin-top: 8px;"></textarea><button type="button"  pid="'+str(i.id)+'" class="btn btn-info huifu-click" style="display: block;margin-top: 3px;">回复</button></div></div>'
            else:
                p_user = Comment.objects.get(id=i.pid.id).userid.username
                html += '<div class="son-comment">' + username +' @ ' +p_user+':&nbsp;&nbsp;' + content + '<div style="maigin-top:2px;line-height: 16px;font-size:12px;color: #808080;">' + date + '<div style="width: 46px;float: right;"> <a class="a_huifu aa_huifu" style="cursor: pointer;">回复</a> </div></div><div class="huifu hide" ><textarea  style="width: 100%;height: 60px;margin-top: 8px;"></textarea><button type="button"  pid="'+str(i.id)+'" class="btn btn-info huifu-click" style="display: block;margin-top: 3px;">回复</button></div></div>'
        data={"status":200,'html':mark_safe(html),'pid':pid}
        return JsonResponse(data)

def comment_subject(request):
    if request.method == "GET":
        pid = int(request.GET.get("pid"))
        user = request.u
        content = request.GET.get("content")
        s_id = request.GET.get("s_id")
        if pid == 0:
            Comment.objects.create(content=content, pid=None, subjectid=Subject.objects.get(id=s_id), userid=user)
        else:
            Comment.objects.create(content=content, pid=Comment.objects.get(id=pid), subjectid=Subject.objects.get(id=s_id), userid=user)
        data = {"status":200}
        return JsonResponse(data)

def shenqing_jz(request):
    if request.method == "GET":
        user = request.u
        if user.is_heshi == False:
            return JsonResponse({"status":404})
        pd = int(request.GET.get("pd"))
        s_id = request.GET.get("s_id")
        sid=Subject.objects.get(id=s_id)
        tel = request.GET.get("tel", None)

        if pd ==0 :
            if tel == None:
                return JsonResponse({"status": 201})
            ret = re.match(r"^1[35678]\d{9}$", tel)
            if not ret:
                return JsonResponse({"status":201})
            elif  ret:
                if len(Usertojob.objects.filter(sid=sid, uid=request.u)) == 0:
                    Usertojob.objects.create(status=0,u_tel=tel,sid=sid,uid=request.u, for_pass=0)
        elif pd == 1:
            Usertojob.objects.filter(sid=sid, uid=request.u).delete()

        return JsonResponse({"status":200})

def jubao(request):
    if request.method == "GET":
        try :
            sid = request.GET.get("sid")
            content = request.GET.get("content")
            user = request.u
            Report.objects.create(uid=user,sid=Subject.objects.get(id=sid), content=content)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

def sfhs(request):
    if request.method == "GET":
        user = request.u
        if int(user.is_heshi) == 1:
            return HttpResponse("<script>alert('该用户已完成认证！');window.open('/index/','_self');</script>")
        return  render(request, "sfhs.html", locals())

def upload_img_z(request):
    user = request.u
    if int(user.is_heshi) == 1:
        return HttpResponse("<script>alert('该用户已完成认证！');window.open('/index/','_self');</script>")
    allow_suffix = ['jpg', 'png', 'jpeg', 'bmp']
    file = request.FILES.get('pic_z')
    file_suffix = file.name.split(".")[-1]
    user = request.u
    if file_suffix not in allow_suffix:
        return HttpResponse("<script>alert('格式仅支持jpg,jpeg,bmp,png');window.open('/sfhs/','_self');</script>")
    file_name = str(uuid.uuid1()) + "." + file_suffix
    file_path = os.path.join(settings.IDCARD_PARH, 'images',file_name)
    file_url = os.path.join(settings.IDCARD_URL, 'images', file_name)
    with open(file_path, 'wb') as f:
        for i in file.chunks():
            f.write(i)
            f.close()
    User.objects.filter(id=user.id).update(idcardpath=file_url)
    return HttpResponse("<script>alert('上传成功！');window.open('/sfhs/','_self');</script>")

def upload_img_t(request):
    user = request.u
    allow_suffix = ['jpg', 'png', 'jpeg', 'bmp']
    file = request.FILES.get('pic_t')
    file_suffix = file.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return HttpResponse("<script>alert('格式仅支持jpg,jpeg,bmp,png');window.open('/grzl/','_self');</script>")
    file_name = str(uuid.uuid1()) + "." + file_suffix
    file_path = os.path.join(settings.IDCARD_PARH, 'images',file_name)
    file_url = os.path.join(settings.IDCARD_URL, 'images', file_name)
    print(file_path)
    with open(file_path, 'wb') as f:
        for i in file.chunks():
            f.write(i)
            f.close()
    User.objects.filter(id=user.id).update(imagepath=file_url)
    return HttpResponse("<script>alert('上传成功！');window.open('/grzl/','_self');</script>")

def upload_img_f(request):
    user = request.u
    if int(user.is_heshi) == 1:
        return HttpResponse("<script>alert('该用户已完成认证！');window.open('/index/','_self');</script>")
    allow_suffix = ['jpg', 'png', 'jpeg', 'bmp']
    file = request.FILES.get('pic_f')
    file_suffix = file.name.split(".")[-1]
    user = request.u
    if file_suffix not in allow_suffix:
        return HttpResponse("<script>alert('格式仅支持jpg,jpeg,bmp,png');window.open('/sfhs/','_self');</script>")
    file_name = str(uuid.uuid1()) + "." + file_suffix
    file_path = os.path.join(settings.IDCARD_PARH, 'images',file_name)
    file_url = os.path.join(settings.IDCARD_URL, 'images', file_name)
    with open(file_path, 'wb') as f:
        for i in file.chunks():
            f.write(i)
            f.close()
    User.objects.filter(id=user.id).update(idcardpath1=file_url)
    return HttpResponse("<script>alert('上传成功！');window.open('/sfhs/','_self');</script>")

def upload_img_y(request):
    user = request.u
    if int(user.is_heshi) == 1:
        return HttpResponse("<script>alert('该用户已完成认证！');window.open('/index/','_self');</script>")
    if int(user.usertype) != 1:
        return HttpResponse("<script>alert('该用户类型必须为商铺！');window.open('/index/','_self');</script>")
    allow_suffix = ['jpg', 'png', 'jpeg', 'bmp']
    file = request.FILES.get('pic_y')
    file_suffix = file.name.split(".")[-1]
    user = request.u
    if file_suffix not in allow_suffix:
        return HttpResponse("<script>alert('格式仅支持jpg,jpeg,bmp,png');window.open('/sfhs/','_self');</script>")
    file_name = str(uuid.uuid1()) + "." + file_suffix
    file_path = os.path.join(settings.IDCARD_PARH, 'images',file_name)
    file_url = os.path.join(settings.IDCARD_URL, 'images', file_name)
    with open(file_path, 'wb') as f:
        for i in file.chunks():
            f.write(i)
            f.close()
    User.objects.filter(id=user.id).update(yingyezhizhao=file_url)
    return HttpResponse("<script>alert('上传成功！');window.open('/sfhs/','_self');</script>")

def wyfb(request):
    user = request.u
    if int(user.is_heshi) == 0:
        return HttpResponse("<script>alert('请先认证！');window.open('/sfhs/','_self');</script>")
    if int(user.xinyong) <60:
        return HttpResponse("<script>alert('当前信用值不足，请联系管理员充值！');window.open('/sfhs/','_self');</script>")
    if request.method == "GET":
        wagetp = Wages.objects.all()
        worktp = Captrue.objects.all()
        return render(request,"wyfb.html",locals())

    elif request.method == "POST":
        title = return_val(request.POST.get("title"))
        usertp = int(request.POST.get("usertp"))
        if usertp == 1 or usertp == 2:
            wagetp = request.POST.get("wagetp")
            worktp = request.POST.get("worktp")
            tel = return_val(request.POST.get("tel"))
            place = return_val(request.POST.get("place"))
            desc = return_val(request.POST.get("desc"))
            if title == 0 or tel == 0 or place == 0 or desc == 0 or desc == 0:
                return HttpResponse("<script>alert('字符不能输入为空！');window.open('/wyfb/','_self');</script>")
            ret = re.match(r"^1[35678]\d{9}$", tel)
            if not ret:
                return HttpResponse("<script>alert('手机格式错误！');window.open('/wyfb/','_self');</script>")
            if user.usertype == 1:
                Subject.objects.create(title=title, s_tel=tel,place=place,desc=desc,shenhe=1,xiajia=0,usertype=usertp,status=1,user=User.objects.get(id=user.id),wages=Wages.objects.get(id=wagetp),worktype=Captrue.objects.get(id=worktp))
                return HttpResponse("<script>alert('发布成功！');window.open('/wyfb/','_self');</script>")
            elif user.usertype == 0:
                Subject.objects.create(title=title, s_tel=tel,place=place,desc=desc,shenhe=0,xiajia=0,usertype=usertp,status=0,user=User.objects.get(id=user.id),wages=Wages.objects.get(id=wagetp),worktype=Captrue.objects.get(id=worktp))
                return HttpResponse("<script>alert('发布成功！');window.open('/wyfb/','_self');</script>")
            else:
                return HttpResponse("<script>alert('发布失败！');window.open('/wyfb/','_self');</script>")
        else:
            return redirect(reverse("wyfb"))

def grzl(request):
    if request.method == "GET":
        return render(request, "grzl.html", locals())
    elif request.method == "POST":
        sex_select = request.POST.get("sex_select", None)
        username = request.POST.get("username", None)
        if sex_select != None:
            sex_select_int = int(sex_select)
            if sex_select_int == 1 or sex_select_int == 2 or sex_select_int == 3:
                User.objects.filter(id=request.u.id).update(sex=sex_select_int)
                return HttpResponse("<script>alert('修改成功');window.open('/grzl/','_self');</script>")
            else:
                return HttpResponse("<script>alert('未知错误');window.open('/grzl/','_self');</script>")
        if username != None:
            if len(username) > 8:
                return HttpResponse("<script>alert('昵称太长！请重试！');window.open('/grzl/','_self');</script>")
            if len(username) < 4:
                return HttpResponse("<script>alert('昵称太短！请重试！');window.open('/grzl/','_self');</script>")
            User.objects.filter(id=request.u.id).update(username=username)
            return HttpResponse("<script>alert('修改成功');window.open('/grzl/','_self');</script>")
        return  redirect(reverse("grzl"))

def wdfb(request):

    user = request.u
    articless = Subject.objects.filter(user=user).all()
    p = int(request.GET.get("p", 1))
    for_page_count = 10
    articles = articless[(p - 1) * for_page_count:p * for_page_count]
    data_count = len(articless)
    page = PageArticle(data_count, for_page_count, p, "/wdfb")
    pagestr = page.page_list()
    return render(request, "wdfb.html", locals())

def article_update(request):
    user = request.u
    if int(user.is_heshi) == 0:
        return HttpResponse("<script>alert('请先认证！');window.open('/sfhs/','_self');</script>")
    if int(user.xinyong) <60:
        return HttpResponse("<script>alert('当前信用值不足，请联系管理员充值！');window.open('/wdfb/','_self');</script>")
    if request.method == "GET":
        sid = request.GET.get("sid")
        wagetp = Wages.objects.all()
        worktp = Captrue.objects.all()
        article = Subject.objects.filter(id=sid, user=user).first()
        select_wages = '<select name = "wagetp" id = "wagetp" >'
        for i in wagetp:
            select_wages += '<option value="'
            select_wages += str(i.id)
            select_wages += '"'
            if int(i.id) == int(article.wages.id):
                select_wages += 'selected'
            select_wages += '>'
            select_wages += i.name
            select_wages += '</option>'
        select_wages += '</select>'
        select_wages = mark_safe(select_wages)

        select_worktp = '<select name = "worktp" id = "worktp" >'
        for i in worktp:
            select_worktp += '<option value="'
            select_worktp += str(i.id)
            select_worktp += '"'
            if int(i.id) == int(article.worktype.id):
                select_worktp += 'selected'
            select_worktp += '>'
            select_worktp += i.name
            select_worktp += '</option>'
        select_worktp += '</select>'
        select_worktp = mark_safe(select_worktp)
        return render(request, "article_update.html", locals())

    elif request.method == "POST":
        title = return_val(request.POST.get("title"))
        usertp = int(request.POST.get("usertp"))
        sid = int(request.POST.get("sid"))
        old_path = reverse("article_update") + "?id=" + str(sid)
        if usertp == 1 or usertp == 2:
            wagetp = request.POST.get("wagetp")
            worktp = request.POST.get("worktp")
            tel = return_val(request.POST.get("tel"))
            place = return_val(request.POST.get("place"))
            desc = return_val(request.POST.get("desc"))
            if title == 0 or tel == 0 or place == 0 or desc == 0 or desc == 0:
                return HttpResponse("<script>alert('字符不能输入为空！');window.open('"+old_path+"','_self');</script>")
            ret = re.match(r"^1[35678]\d{9}$", tel)
            if not ret:
                return HttpResponse("<script>alert('手机格式错误！');window.open('"+old_path+"','_self');</script>")
            Subject.objects.filter(id=sid, user=user).update(title=title, s_tel=tel,place=place,desc=desc,usertype=usertp,wages=Wages.objects.get(id=wagetp),worktype=Captrue.objects.get(id=worktp))
            return HttpResponse("<script>alert('修改成功！');window.open('/wdfb/','_self');</script>")
        else:
            return redirect(old_path)

def article_del(request):
    if request.method == "GET":
        sid = request.GET.get("sid")
        Subject.objects.filter(id=sid, user=request.u).delete()
        return JsonResponse({"status":200})

def article_xiajia(request):
    user = request.u
    if int(user.is_heshi) == 0:
        return HttpResponse("<script>alert('请先认证！');window.open('/sfhs/','_self');</script>")
    if int(user.xinyong) <60:
        return HttpResponse("<script>alert('当前信用值不足，请联系管理员充值！');window.open('/wdfb/','_self');</script>")
    if request.method == "GET":
        sid = request.GET.get("sid")
        xiajia = int(request.GET.get("xiajia"))
        if xiajia == 1:
            Subject.objects.filter(id=sid, user=request.u).update(xiajia=xiajia)
        elif xiajia == 0:
            Subject.objects.filter(id=sid, user=request.u).update(xiajia=xiajia)
        return JsonResponse({"status":200})

def usertojob(request):
    user = request.u
    if int(user.is_heshi) == 0:
        return HttpResponse("<script>alert('请先认证！');window.open('/sfhs/','_self');</script>")
    if int(user.xinyong) <60:
        return HttpResponse("<script>alert('当前信用值不足，请联系管理员充值！');window.open('/wdfb/','_self');</script>")
    if request.method == "GET":
        sid = request.GET.get("sid")
        article = Subject.objects.filter(id=sid, user=request.u).first()
        ujs = article.usertojob_set.filter(status=0).all()
        return render(request, "usertojob.html", locals())

    elif request.method == "POST":
        sid = request.POST.get("sid")
        pd = request.POST.get("pd")
        uid = request.POST.get("uid")
        s = Subject.objects.get(id=sid)
        if str(s.user.id) != str(user.id):
            return JsonResponse({"status":404})
        Usertojob.objects.filter(sid=s, uid=User.objects.get(id=uid)).update(status=1,for_pass=pd)
        #给双方发通知
        uj = Usertojob.objects.get(sid=s, uid=User.objects.get(id=uid))
        s_tel = s.s_tel
        u_tel = uj.u_tel
        if int(pd) == 1:
            content_notice_u = '您申请的"'+str(s.title)+'"已经通过，请及时联系：'+str(s_tel)
            content_notice_s = '该申请用户"'+str(User.objects.get(id=uid).username)+'"联系方式为：' + str(s_tel)
            Notice.objects.create(title="【系统通知】", content=content_notice_u, user=User.objects.get(id=uid))
            Notice.objects.create(title="【系统通知】", content=content_notice_s, user=user)
        elif int(pd) == 0:
            content_notice_u = '您申请的"' + str(s.title) + '"未通过。'
            Notice.objects.create(title="【系统通知】", content=content_notice_u, user=User.objects.get(id=uid))
        return JsonResponse({"status":200})

def xxzx(request):
    if request.method == "GET":
        user = request.u
        tp = int(request.GET.get("tp", 1))
        if tp == 1:
            rows = Notice.objects.filter(user=user).order_by("-datetime")
            return render(request, "xxzx.html", locals())
        elif tp ==2:

            rows = []
            articles = Subject.objects.filter(user=user).order_by("-date")
            for i in articles:
                r= Comment.objects.filter(pid=None, subjectid=i).order_by("-date")
                for j in r:
                    rows.append(j)

            rs = Comment.objects.filter(userid=user).order_by("-date")
            for k in rs:
                l = Comment.objects.filter(pid=k).order_by("-date")
                for z in l:
                    rows.append(z)
            return render(request, "hfzx.html",locals())

def notice(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        if user_id:
            try:
                u = User.objects.get(id=user_id)
                request.u = u
            except:
                request.session.flush()
        nid = request.GET.get("nid", None)
        if nid:
            res = Notice.objects.filter(id=nid, user=None).first()
            return render(request, "notice.html", locals())
        else:
            res = Notice.objects.filter(user=None).all()
            return render(request, "all_notice.html", locals())

def lxwm(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            u = User.objects.get(id=user_id)
            request.u = u
        except:
            request.session.flush()
    return render(request, "lxwm.html")