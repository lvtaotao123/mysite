from django import forms
from django.forms import widgets
from partjob.models import Wages, Captrue

class ArticleForm(forms.Form):
    title = forms.CharField(min_length=4,max_length=20,label="文章标题", error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*最低长度不能少于4位',
        'max_length': '*最低长度不能多于20位',
    },
        widget = widgets.TextInput(attrs={"class": "form-control input-sm duiqi", "name":"title"})
    )
    place = forms.CharField(min_length=2, label="工作地点", error_messages={
        "requried":"*该字段不能为空",
        "min_length": "*最低字段不能少于2位",
    },
        widget= widgets.TextInput(attrs={"class": "form-control input-sm duiqi", "name":"place"})
    )
    desc = forms.CharField(min_length=6,label="工作描述",error_messages={
        "requried":"*该字段不能为空",
        "min_length": "*最低字段不能少于6位",
    },
        widget=widgets.Textarea(attrs={"class": "form-control input-sm duiqi", "name": "desc"})
   )
    tp = forms.ChoiceField(
        label="帖子类型",
        choices= ((1, "招人"),(2,"求职")),
        initial=1,
        widget=widgets.Select(attrs={"class":"form-control select-duiqi", "name":"tp"})
    )
    worktp = forms.ModelChoiceField(label="工作类型",queryset=Captrue.objects.all(), required=True, initial=1,widget=widgets.Select(attrs={"class":"form-control select-duiqi", "name":"worktp"}))

    wagetp = forms.ModelChoiceField(label="工资范围",queryset=Wages.objects.all(), required=True, initial=1,widget=widgets.Select(attrs={"class":"form-control select-duiqi", "name":"wagetp"}))

class Update_pwd(forms.Form):
     old_pwd = forms.CharField(min_length=6,max_length=16,label="原密码", error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*最低长度不能少于6位',
        'max_length': '*最低长度不能多于16位',
        }, widget=widgets.PasswordInput(attrs={"class": "form-control input-sm duiqi", "name": "old_pwd"})
        )

     new_pwd1 = forms.CharField(min_length=6, max_length=16, label="新密码", error_messages={
         "requried": "*该字段不能为空",
         'min_length': '*最低长度不能少于6位',
         'max_length': '*最低长度不能多于16位',
        }, widget=widgets.PasswordInput(attrs={"class": "form-control input-sm duiqi", "name": "new_pwd1"})
        )

     new_pwd2 = forms.CharField(min_length=6, max_length=16, label="确定密码", error_messages={
         "requried": "*该字段不能为空",
         'min_length': '*最低长度不能少于6位',
         'max_length': '*最低长度不能多于16位',
        }, widget=widgets.PasswordInput(attrs={"class": "form-control input-sm duiqi", "name": "new_pwd2"})
        )

class User_form(forms.Form):
    username = forms.CharField(min_length=4,max_length=8, error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*最低长度不能少于4位',
        'max_length': '*最低长度不能多于8位',
    },
        widget = widgets.TextInput(attrs={"placeholder": "请输入用户名", "name":"username","id":"username"})
    )

    password = forms.CharField(min_length=6,max_length=16, error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*最低长度不能少于6位',
        'max_length': '*最低长度不能多于16位',
    },
        widget = widgets.PasswordInput(attrs={"placeholder": "请输入密码:只包含a-z A-Z 0-9 . _", "name":"password","id":"password"})
    )
    confirm_pwd = forms.CharField(min_length=6,max_length=16, error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*最低长度不能少于6位',
        'max_length': '*最低长度不能多于16位',
    },
        widget = widgets.PasswordInput(attrs={"placeholder": "请确认密码", "name":"confirm_pwd","id":"confirm_pwd"})
    )

    email = forms.EmailField(
        error_messages={
            "requried": "*该字段不能为空",
        },
        widget = widgets.EmailInput(attrs={"placeholder": "请输入电子邮箱", "name":"email","id":"email"})
    )

    mobile = forms.CharField(min_length=11,max_length=11, error_messages={
        "requried": "*该字段不能为空",
        'min_length': '*手机格式错误',
        'max_length': '*手机格式错误',
    },
        widget = widgets.TextInput(attrs={"placeholder": "请输入手机", "name":"mobile","id":"mobile"})
    )

    token = forms.CharField( error_messages={
        "requried": "*该字段不能为空",

    },
        widget = widgets.TextInput(attrs={"placeholder": "请输入验证码", "name":"token","id":"token"})
    )
