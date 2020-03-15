from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from partjob import models
from utils.page_list import Page
from django.utils import timezone
from django.forms import fields
import json
from django.db.models import Q
from  django.forms import widgets
from django.utils.safestring import mark_safe
from utils.myform import *
# Create your views here.
from django.urls import reverse
import datetime
from django.contrib.auth.hashers import make_password

def all_user(request):#用户管理
    p = int(request.GET.get('p', 1))
    if request.method == 'GET':
        for_page_count = 8
        userss = models.User.objects.all().order_by('-register_date', '-lastlogin_date')
        users = userss[(p-1)*for_page_count:p*for_page_count]
        data_count = len(userss)
        page = Page(data_count, for_page_count, p)
        pagestr = page.page_list()
    return render(request, 'admin_page/all_user.html',{'users':users, 'pagestr':pagestr})

def ajax_user(request):
    data = {'data':"评论失败！"}
    uid = request.POST.get("uid")
    user = models.User.objects.filter(id=uid).first()
    data['username'] = user.username
    data['tel'] = user.tel
    if user.usertype == 0:
        data['usertype'] = "学生"
    else:
        data['usertype'] = "商铺"
    data['imagepath'] = str(user.imagepath)
    if user.sex == 0:
        data['sex'] = "保密"
    elif user.sex == 1:
        data['sex'] = "女"
    else:
        data['sex'] = "男"
    data['xinyong'] = user.xinyong
    data['money'] = user.money
    data['register'] = user.register_date.strftime("%Y-%m-%d %H:%M:%S")
    data['last'] = user.lastlogin_date.strftime("%Y-%m-%d %H:%M:%S")
    if user.is_heshi == 0:
        data['heshi'] = '未核实'
    else :
        data['heshi'] = '核实'
    data["data"] = "评论成功！"
    return HttpResponse(json.dumps(data))

def ajax_article(request):
    data = {"status":"修改失败"}
    aid = request.POST.get("aid")
    data["aid"] = aid
    article = models.Subject.objects.filter(id=aid).first()
    data['title'] = '<input type="text" maxlength="20" minlength="4" required class="form-control input-sm duiqi" name="title" value="{}">'.format(article.title)
    data['place'] = '<input type="text"  minlength="2" required class="form-control input-sm duiqi" name="place" value="{}">'.format(article.place)
    data['desc'] = '<textarea class="form-control duiqi " name="desc">{}</textarea>'.format(article.title)
    work = '<select class="form-control select-duiqi" name="worktp">'
    for i in models.Captrue.objects.all():

        if str(i.name) == str(article.worktype):
            work += '<option value="{}" selected>{}</option>'.format(i.id, i.name)
        else:
            work += '<option value="{}">{}</option>'.format(i.id, i.name)

    work += "</select>"
    wagetp = '<select class="form-control select-duiqi" name="wagetp">'
    for i in models.Wages.objects.all():
        if str(i.name) == str(article.wages):
            wagetp += '<option value="{}" selected>{}</option>'.format(i.id, i.name)
        else:
            wagetp += '<option value="{}">{}</option>'.format(i.id, i.name)
    wagetp += "</select>"
    data['work'] = work
    data['wagetp'] = wagetp
    if article.usertype == 1:
        data['tp'] = '<select class="form-control select-duiqi" name="tp"><option value="1" selected>招人</option><option value="2">求职</option></select>'
    else :
        data['tp'] = '<select class="form-control select-duiqi" name="tp"><option value="1" >招人</option><option value="2" selected>求职</option></select>'
    data['author'] = article.user.username
    data['count'] = article.usertojob_set.all().count()

    passed = []
    passd = article.usertojob_set.filter(for_pass = 1).all()
    for i in passd:
        passed.append(i.uid.username)
    j = len(passed)
    if j == 0:
        data['pass'] = "无"
    else:
        data['pass'] = ','.join(passed)
        data['pass'] += '(共{}人)'.format(j)
    data['date'] = article.date.strftime("%Y-%m-%d %H:%M:%S")
    if article.shenhe:
        data['shenhe'] = '审核成功'
    else:
        data['shenhe'] = '审核未通过'

    return HttpResponse(json.dumps(data))

def add_user(request):
    dic = {'error':1,'message':'请求失败'}
    if request.method == 'POST':
        name = request.POST['sName']
        pwd = request.POST['pwd']
        tel = request.POST['tel']
        leibie = request.POST['leibie']
        sex = request.POST['sex']
        images = '/static/pic/user_image.jpg'
        models.User.objects.create(username=name, password=make_password(pwd), tel=tel,usertype=leibie, imagepath=images, sex=sex, xinyong=100, idcardpath1='',idcardpath='')
        return redirect('/admin/all_user')

def del_user(request):
    data = {'data':'删除失败！'}
    try:
        uid = request.POST.get("uid")
        models.User.objects.filter(id=uid).delete()
        data['data'] = "删除成功！"
    except:
        return  HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps(data))

def del_article(request):
    data = {'data':'删除失败！'}
    try:
        aid = request.POST.get("aid")
        models.Subject.objects.filter(id=aid).delete()
        data['data'] = "删除成功！"
    except:
        return  HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps(data))

def user_input(request):
    if request.method == 'POST':
        d = request.POST.get("input_value")
        data = models.User.objects.filter(username =d)
        data1 = models.User.objects.filter(tel = d)
        data = data | data1

        return render(request, 'admin_page/all_user.html', {'users': data,'callback':mark_safe('<a class="btn btn-yellow btn-xs" data-toggle="modal"  href="/admin/all_user">返回全体用户 </a>')})

def shenhe_input(request):
    if request.method == 'POST':
        d = request.POST.get("input_value")
        data = models.User.objects.filter(username =d,status=1)
        data1 = models.User.objects.filter(tel = d, status=1)
        data = data | data1

        return render(request, 'admin_page/user_shenhe.html', {'users': data,'callback':mark_safe('<a class="btn btn-yellow btn-xs" data-toggle="modal"  href="/admin/user_shenhe">返回全体用户 </a>')})


def show_xinyong(request):
    if request.method == "POST":
        data = {}
        uid = request.POST.get("uid")
        user = models.User.objects.filter(id=uid).first()
        data["username"] = user.username
        data["xinyong"] = user.xinyong
        data["input"] = "每次违规扣取50信用点"
        data["uid"] = uid
        return HttpResponse(json.dumps(data))

def add_xinyong(request):
    data = {"data":"充值失败！"}
    if request.method == "POST":
        uid = request.POST.get("x_uid")
        old = request.POST.get("old_xinyong")
        i = request.POST.get("x_i")
        xy = int(old) + int(i)
        models.User.objects.filter(id=uid).update(xinyong=xy)
        return redirect("/admin/all_user")

def user_shenhe(request):#用户审核
    if request.method == 'GET':
        p = int(request.GET.get('p', 1))
        userss = models.User.objects.filter(status=0, is_heshi=0)
        for_page_count = 8
        users = userss[(p - 1) * for_page_count:p * for_page_count]
        data_count = len(userss)
        page = Page(data_count, for_page_count, p)
        pagestr = page.page_list()
        return render(request, 'admin_page/user_shenhe.html',{'users':users, 'pagestr':pagestr})

    elif request.method == 'POST':
        data = {}
        try:
            uid = request.POST.get("uid")
            pd = int(request.POST.get("pd"))
            if pd == 1:
                models.User.objects.filter(id=uid).update(is_heshi = 1, status=1)
            else:
                models.User.objects.filter(id=uid).update(status=1)
            data['data'] = '审核成功'
            return HttpResponse(json.dumps(data))
        except:
            data['data'] = "审核失败！请重新提交"
            return HttpResponse(json.dumps(data))

def article_input(request):
    if request.method == 'POST':
        d = request.POST.get("input_value")
        try:
            uid = models.User.objects.get(username=d).id
        except:
            uid = -1
        data = models.Subject.objects.filter(Q(title =d) | Q(user = uid))
        return render(request, 'admin_page/all_article.html', {'articles': data,'callback':mark_safe('<a class="btn btn-yellow btn-xs" data-toggle="modal"  href="/admin/all_article">返回全部帖子 </a>')})

def all_article(request):
    if request.method == "GET":
        fm = ArticleForm()
        p = int(request.GET.get('p', 1))
        for_page_count = 8
        articless = models.Subject.objects.all().order_by('-date')
        articles = articless[(p - 1) * for_page_count:p * for_page_count]
        data_count = len(articless)
        page = Page(data_count, for_page_count, p, "/admin/all_article")
        pagestr = page.page_list()

        return render(request,"admin_page/all_article.html", locals())

    elif request.method == "POST":
        fm = ArticleForm()
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            models.Subject.objects.create(title=data["title"], place=data["place"], desc=data["desc"], usertype=data["tp"], user_id=21, wages_id=models.Wages.objects.get(name = data["wagetp"]).id, worktype_id=models.Captrue.objects.get(name = data["worktp"]).id)
        return redirect("/admin/all_article")

def update_article(request):
    if request.method == "POST":
        data = request.POST
        aid = data["aid"]
        title = data["title"]
        place = data["place"]
        desc = data["desc"]
        wagetp = data["wagetp"]
        worktp = data["worktp"]
        tp = data["tp"]
        models.Subject.objects.filter(id =aid).update(title=title,place=place,desc=desc,wages=wagetp,worktype=worktp,usertype=tp)
        return redirect('/admin/all_article')

def article_shenhe(request):
    if request.method == "GET":
        p = int(request.GET.get('p', 1))
        wages = int(request.GET.get('wages', 0))
        worktp = int(request.GET.get('worktp', 0))
        for_page_count = 8
        wages_select = '<select class=" form-control" id="select_wages"><option value="0" >全部</option>'
        worktp_select = '<select class=" form-control" id="select_worktp"><option value="0" >全部</option>'
        if wages == 0 and worktp == 0:
            wages_select = '<select class=" form-control" id="select_wages"><option value="0" selected>全部</option>'
            worktp_select = '<select class=" form-control" id="select_worktp"><option value="0" selected>全部</option>'
            articless = models.Subject.objects.filter(shenhe=0,status=0).order_by('-date')
        elif wages == 0 and worktp != 0:
            wages_select = '<select class=" form-control" id="select_wages"><option value="0" selected>全部</option>'
            articless = models.Subject.objects.filter(worktype=worktp,shenhe=0,status=0).order_by('-date')
        elif wages != 0 and worktp == 0:
            worktp_select = '<select class=" form-control" id="select_worktp"><option value="0" selected>全部</option>'
            articless = models.Subject.objects.filter(wages=wages,shenhe=0,status=0).order_by('-date')
        else:
            articless = models.Subject.objects.filter(wages=wages, worktype=worktp,shenhe=0,status=0).order_by('-date')
        articles = articless[(p - 1) * for_page_count:p * for_page_count]
        data_count = len(articless)
        page = Page(data_count, for_page_count, p, "/admin/article_shenhe")
        pagestr = page.page_list()
        w = models.Wages.objects.all()
        c = models.Captrue.objects.all()
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
        worktp_select += '</select>'
        wages_select = mark_safe(wages_select)
        worktp_select = mark_safe(worktp_select)
        return render(request,"admin_page/article_shenhe.html", locals())

    elif request.method == 'POST':
        data = {}
        try:
            aid = request.POST.get("aid")
            pd = int(request.POST.get("pd"))
            print(aid, pd)
            if pd == 1:
                models.Subject.objects.filter(id=aid).update(shenhe = 1, status=1)
            else:
                models.Subject.objects.filter(id=aid).update(shenhe = 0,status=1)
            data['data'] = '审核成功'
            return HttpResponse(json.dumps(data))
        except:
            data['data'] = "审核失败！请重新提交"
            return HttpResponse(json.dumps(data))

def find_shenhe(request):
    if request.method == 'POST':
        last_path = request.POST.get("url_info")
        content = request.POST.get("txt")
        try:
            uid = models.User.objects.get(username=content).id
        except:
            uid = -1
        articles = models.Subject.objects.filter(Q(title =content) | Q(user = uid), shenhe=0,status=0)
        return render(request, 'admin_page/findshenhe_article.html',locals())

def add_wages(request):
    if request.method == "POST":
        v = request.POST.get("tag", 0)
        wages = request.POST.get("wages")
        models.Wages.objects.create(name=wages)
        if str(v) == '1':
            return redirect('/admin/tags/')
        return redirect('/admin/article_shenhe/')

def add_worktp(request):
    if request.method == "POST":
        v = request.POST.get("tag", 0)
        worktp = request.POST.get("worktp")
        models.Captrue.objects.create(name=worktp)
        if str(v) == '1':
            return redirect('/admin/tags/')
        return redirect('/admin/article_shenhe/')

def shenhe_ajax(request):
    if request.method == 'POST':
        try:
            data={}
            aid = request.POST.get("aid")
            d = models.Subject.objects.filter(id=aid).first()
            data['title'] = d.title
            data['place'] = d.place
            data['desc'] = d.desc
            data['date'] = d.date.strftime("%Y-%m-%d %H:%M:%S")
            data['tp'] = int(d.usertype)
            data['wages'] = d.wages.name
            data['worktp'] = d.worktype.name
            data['data'] = "审核成功"
            data['id'] = aid
            return HttpResponse(json.dumps(data))
        except:
            data['data'] = "审核失败！请重新提交"
            return HttpResponse(json.dumps(data))

def tags(request):
    if request.method == 'GET':
        wages = models.Wages.objects.all()
        worktps = models.Captrue.objects.all()
        return render(request, 'admin_page/tags.html', locals())

def update_worktp1(request):
    if request.method == 'POST':
        data = {}
        try:
            cid = request.POST.get('cid')
            d = models.Captrue.objects.filter(id=cid).first()
            data['name'] = d.name
            data['id'] = cid
            data['data'] = "success"
        except:
            data['data'] = "fail"
        print(data)
        return HttpResponse(json.dumps(data))

def update_worktp(request):
    if request.method == 'POST':
        data = {}
        try:
            cid = request.POST.get('tag_worktp_input')
            name = request.POST.get('worktp')
            print(cid, name)
            models.Captrue.objects.filter(id=cid).update(name=name)
            data['data'] = "success"
        except:
            data['data'] = "fail"
        print(data)
        return redirect('/admin/tags/')


def update_wages1(request):
    if request.method == 'POST':
        data = {}
        try:
            wid = request.POST.get('wid')
            d = models.Wages.objects.filter(id=wid).first()
            data['name'] = d.name
            data['id'] = wid
            data['data'] = "success"
        except:
            data['data'] = "fail"
        return HttpResponse(json.dumps(data))

def update_wages(request):
    if request.method == 'POST':
        data = {}
        try:
            wid = request.POST.get('tag_wages_input')
            name = request.POST.get('wages')
            print(wid, name)
            models.Wages.objects.filter(id=wid).update(name=name)
            data['data'] = "success"
        except:
            data['data'] = "fail"
        return redirect('/admin/tags/')

def del_wages(request):
    if request.method == "POST":
        data = {'data': 'fail'}
        try:
            wid = request.POST.get("wid")
            dd = models.Wages.objects.get(id=wid)
            if dd.subject_set.count() != 0:
                data['data'] = '当前标签内包含贴子，如要删除联系站长！'
                return HttpResponse(json.dumps(data))
            dd.delete()
            data['data'] = '删除成功'
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(json.dumps(data))

def del_worktp(request):
    if request.method == "POST":
        data = {'data': 'fail'}
        try:
            cid = request.POST.get("cid")
            dd = models.Captrue.objects.get(id=cid)
            if dd.subject_set.count() != 0:
                data['data'] = '当前标签内包含贴子，如要删除联系站长！'
                return HttpResponse(json.dumps(data))
            dd.delete()
            data['data'] = '删除成功'
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(json.dumps(data))

def weigui(request):
    if request.method == "GET":
        p = int(request.GET.get('p', 1))
        for_page_count = 8
        reportss = models.Report.objects.filter(status=0, is_no=0).order_by('datetime')
        reports = reportss[(p - 1) * for_page_count:p * for_page_count]
        data_count = len(reportss)
        page = Page(data_count, for_page_count, p, '/admin/weigui')
        pagestr = page.page_list()
        return render(request, 'admin_page/weigui.html', locals())

    elif request.method == "POST":
        data = {"data":"fail"}
        # try:
        rid = request.POST.get("rid")
        pd = request.POST.get("pd")
        models.Report.objects.filter(id=rid).update(status = 1, is_no = pd)
        if int(pd) == 1:
            uid = models.Report.objects.filter(id=rid).first().sid.user.id
            user = models.User.objects.filter(id=uid).first()
            one_xinyong = models.Manages.objects.all().first().one_xinyong
            new_xinyong = int(user.xinyong) - int(one_xinyong)
            new_money = int(user.money) + 1
            user.xinyong=new_xinyong
            user.money=new_money
            user.save()
        data = {"data":"success"}
        return HttpResponse(json.dumps(data))
        # except:
        #     return HttpResponse(json.dumps(data))

def find_report(request):
    if request.method == "POST":
        input = request.POST.get("txt")
        url_info = request.POST.get("url_info")
        try:
            uid = models.User.objects.get(username=input).id
        except:
            uid = -1
        reports = models.Report.objects.filter(Q(uid =uid) | Q(sid__user__id = uid), is_no = 0, status = 0)
        return render(request, 'admin_page/find_report.html',locals())

def manager(request):
    if request.method == 'GET':
        fm = Update_pwd()
        money = models.Manages.objects.all().first().one_xinyong
        return render(request, 'admin_page/manage_user.html', locals())

    elif request.method == "POST":
        fm = Update_pwd()
        password = str(models.Manages.objects.all().first().password)
        form = Update_pwd(request.POST)
        money = models.Manages.objects.all().first().one_xinyong
        if form.is_valid():
            data = form.cleaned_data
            if data["old_pwd"] != password:
                old_error = "*密码错误！"
                return render(request, "admin_page/manage_user.html", locals())
            elif data["new_pwd1"] != data["new_pwd2"]:
                new_error = "*两次密码不匹配！"
                return render(request, "admin_page/manage_user.html", locals())
            elif data["new_pwd1"] == data["new_pwd2"]:
                models.Manages.objects.filter(id=1).update(password=data["new_pwd1"])
                return redirect("/admin/manager")

def manage_money(request):
    if request.method == "POST":
        input = request.POST.get("input_value")
        try:
            input = int(input)
        except:
            return redirect("/admin/manager")
        models.Manages.objects.filter(id=1).update(one_xinyong=input)
        return redirect("/admin/manager")

def add_notice(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        models.Notice.objects.create(title=title,content=content)
        return redirect(reverse("myadmin:notice"))

def login(request):
    if request.method == "GET":
        return render(request, "admin_page/login.html")
    elif request.method == "POST":
        try:
            user = request.POST.get("username")
            pwd = request.POST.get("password")
            u = models.Manages.objects.filter(username = user)
            if u.exists():
                us = u.first()
                if str(pwd) == str(us.password):
                    request.session["admin_id"] = us.id
                    return redirect(reverse("myadmin:all_user"))
            return redirect(reverse("myadmin:admin_login"))
        except:
            return redirect(reverse("myadmin:admin_login"))

def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return redirect(reverse('myadmin:admin_login'))

def notice(request):
    if request.method == 'GET':
        notices = models.Notice.objects.filter(user=None)
        return render(request,"admin_page/notice.html",locals())

def ajax_notice(request):
    if request.method == 'POST':
        nid = request.POST.get("nid")
        n = models.Notice.objects.get(id = nid)
        data={"status":200, "title":n.title, "content":n.content}
        return HttpResponse(json.dumps(data))

def del_notice(request):
    if request.method == 'POST':
        nid = request.POST.get("nid")
        models.Notice.objects.get(id=nid).delete()
        data = {"status": 200}
        return HttpResponse(json.dumps(data))
