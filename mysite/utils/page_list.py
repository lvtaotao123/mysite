from django.utils.safestring import mark_safe

class Page:
    def __init__(self,data_count,for_page_count,current,path='/admin/all_user'):
        self.data_count = data_count
        self.for_page_count = for_page_count
        self.current = int(current)
        self.path = path

    @property
    def max_page(self):
        y, v = divmod(self.data_count, self.for_page_count)
        if v:
            y += 1
        return y


    def page_list(self):
        data_list = ['<footer class="footer"><ul class="pagination"><li><select id="footer">']
        for i in range(1,self.max_page+1):
            page = '<option href="{}/?p={}" value={}>{}</option>'.format(self.path, i, i, i)
            if i == self.current:
                page = '<option href="{}/?p={}" value={} selected>{}</option>'.format(self.path, i,i,i)
            data_list.append(page)
        data_list.append('</select>')
        data_list.append('页</li><li class="gray">共{}页</li>'.format(self.max_page))
        if self.max_page != 0:
            if  self.current == 1:
                data_list.append('<li><i class="glyphicon glyphicon-menu-left"></i></li>')
            else:
                data_list.append('<li><a href="{}/?p={}"><i class="glyphicon glyphicon-menu-left"></i></a></li>'.format(self.path, self.current-1))
            if self.current == self.max_page:
                data_list.append('<li><i class="glyphicon glyphicon-menu-right"></i></li></ul></footer>')
            else:
                data_list.append('<li><a href="{}/?p={}"><i class="glyphicon glyphicon-menu-right"></i></a></li></ul></footer>'.format(self.path, self.current+1))
        else :
            data_list.append('<li><i class="glyphicon glyphicon-menu-left"></i></li>')
            data_list.append('<li><i class="glyphicon glyphicon-menu-right"></i></li></ul></footer>')
        pagestr = mark_safe("".join(data_list))
        return pagestr

class PageArticle():
    def __init__(self,data_count,for_page_count,current,path='/admin/all_user'):
        self.data_count = data_count
        self.for_page_count = for_page_count
        self.current = int(current)
        self.path = path
        self.count = 5

    @property
    def max_page(self):
        y, v = divmod(self.data_count, self.for_page_count)
        if v:
            y += 1
        return y

    @property
    def start(self):
        starts = self.current - int((self.count - 1)/2)
        if starts < 1:
            starts = 1
        return starts

    @property
    def end(self):
        ends = self.start + int(self.count - 1)
        if ends >self.max_page:
            ends = self.max_page
        return ends

    def page_list(self):
        data_list = ['<ul class="pageLink clearfix">']
        if self.max_page > 0:
            if  self.current != 1:
                data_list.append('<li><a href="{}/?p={}" class="prev"><span>上一页</span></a></li>'.format(self.path, self.current-1))

            if self.max_page < self.count:
                for i in range(1, self.max_page + 1):
                    if i == self.current:
                        page = '<li><a class="c linkOn curPage" href="{}/?p={}"><span>{}</span></a></li>'.format(self.path, i, i)
                        data_list.append(page)
                    else:
                        page = '<li><a href="{}/?p={}"><span>{}</span></a></li>'.format(self.path, i, i)
                        data_list.append(page)
            else:
                for i in range(self.start, self.end + 1):
                    if i == self.current:
                        page = '<li><a class="c linkOn curPage" href="{}/?p={}"><span>{}</span></a></li>'.format(self.path, i, i)
                        data_list.append(page)
                    else:
                        page = '<li><a href="{}/?p={}"><span>{}</span></a></li>'.format(self.path, i, i)
                        data_list.append(page)
            if self.current == self.max_page:
                data_list.append('</ul>')
            else:
                data_list.append('<li><a href="{}/?p={}" class="prev"><span>下一页</span></a></li></ul>'.format(self.path, self.current+1))
        else :
            return ""
        pagestr = mark_safe("".join(data_list))
        return pagestr