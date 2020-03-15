from django import template

register = template.Library()

@register.filter
def c_count(m, type):#返回模板中反向查询中筛选的个数 因为不能在模板中实现w.subject_set.filter(usertype=1).count()
    i = 0
    for j in m:
        if str(j.usertype) == str(type):
            i += 1
    return i

@register.filter
def sum(a,b):
    return int(a)+int(b)