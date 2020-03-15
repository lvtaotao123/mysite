from django.db import models

# Create your models here.

class Captrue(models.Model):#工作类别：全职 在校兼职 校外兼职
    name =  models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Wages(models.Model):#工资范围
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Notice(models.Model):#公告栏
    title = models.CharField(max_length=128, default="系统通知:")
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

class User(models.Model):#用户 
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    tel = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    user_choices = ( (1, "商户"),(0, "个人"))
    usertype = models.SmallIntegerField(verbose_name="性别", choices=user_choices)
    imagepath = models.ImageField()
    sex_choices = ( (1, "男"),(2, "女"),(3, "保密"))
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choices)
    xinyong = models.IntegerField()
    money = models.IntegerField(default=0)#违规次数
    register_date = models.DateTimeField(auto_now_add=True)
    lastlogin_date = models.DateTimeField(auto_now=True)
    is_heshi = models.BooleanField(default=False) #身份是否核实
    status =  models.BooleanField(default=False) #是否核实操作过
    idcardpath = models.ImageField()#身份证正面路径
    idcardpath1 = models.ImageField()  # 身份证反面路径
    yingyezhizhao = models.ImageField(default="")#营业执照


    def __str__(self):
        return self.username




class Subject(models.Model):#帖子
    title = models.CharField(max_length=256)
    worktype = models.ForeignKey(to='Captrue', to_field='id', on_delete=models.CASCADE) #工作类别
    wages = models.ForeignKey(to='Wages',to_field='id', on_delete=models.CASCADE) #工资范围
    place = models.CharField(max_length=256)
    desc = models.TextField()
    user = models.ForeignKey(to='User',to_field='id', on_delete=models.CASCADE)
    shenhe = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    xiajia = models.BooleanField(default=False)
    user_choices = ((1, "招人"), (2, "求职"))
    usertype = models.SmallIntegerField(verbose_name="分类", choices=user_choices)
    status = models.BooleanField(default=False)  # 是否核实操作过
    s_tel = models.CharField(max_length=11)
    def __str__(self):
        return self.title


class Comment(models.Model):#评论表
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    pid = models.ForeignKey('self', null=True,  on_delete=models.CASCADE)#父级评论
    userid = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    subjectid = models.ForeignKey(to='Subject',to_field='id', on_delete=models.CASCADE)
    def __str__(self):
        return self.content

class Report(models.Model):#举报表
    uid = models.ForeignKey(to='User',to_field='id', on_delete=models.CASCADE)
    sid = models.ForeignKey(to='Subject', to_field='id', on_delete=models.CASCADE)
    content = models.TextField()
    status = models.BooleanField(default=False)  # 是否举报操作过
    is_no = models.BooleanField(default=False)  # 是否举报成功
    datetime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content

class Usertojob(models.Model):#每个人发布的工作以及申请人
    sid = models.ForeignKey(to='Subject', to_field='id', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    u_tel = models.CharField(max_length=11, null=True)
    for_pass = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Manages(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.fields.EmailField()
    one_xinyong = models.IntegerField()#每次违规扣的信用值


