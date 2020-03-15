import random
from django.template import loader
from django.core.mail import send_mail
from email.header import Header
from partjob import models
from _collections import OrderedDict
from django.shortcuts import HttpResponse

def get_random_six():
    list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z']
    token = random.choice(list)+random.choice(list)+random.choice(list)+random.choice(list)+random.choice(list)+random.choice(list)
    return token

def send_email(token, email_path):
    subject = "246796010@qq.com"
    message = ""
    from_email = "246796010@qq.com"
    recipient_list = [email_path,]
    html = loader.get_template("send_mail.html").render({"token": token})
    return send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,html_message=html)

def find_tree(comment_dict,comment_list):
    for i in comment_dict.keys():
        comments = models.Comment.objects.filter(pid=i).order_by("-date").all()
        last = dict()
        if len(comments) == 0:
            return
        else:
            for j in comments:
                comment_list.append(j)
                last[j.id] = j
            find_tree(last,comment_list)

def build_comment(pid):
    c = models.Comment.objects.order_by("-date").all()
    comments = models.Comment.objects.filter(pid=pid).order_by("-date").all()
    comment_dict = dict()
    comment_list = []
    for i in comments:
        comment_dict[i.id] = i
        comment_list.append(i)
    find_tree(comment_dict,comment_list)
    return comment_list

def return_val(name):
    n = name.strip()
    if len(n) > 0:
        return n
    else:
        return 0


