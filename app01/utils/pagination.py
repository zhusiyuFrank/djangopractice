from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request:     请求对象
        :param queryset:    用户查询的数据
        :param page_size:   每页展示多少条数据
        :param page_param:  页码
        :param plus:        前plus页，后plus页
        """
        get_object = copy.deepcopy(request.GET)
        get_object._mutable = True
        self.get_object = get_object
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        total_user = queryset.count()  # 数据总条数
        # 页码总数
        page_number, div = divmod(total_user, page_size)
        if div:
            page_number += 1
        self.page_number = page_number
        self.plus = plus

    def html(self):

        if self.page_number <= self.plus * 2 + 1:
            start_page = 1
            end_page = self.page_number
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = self.plus * 2 + 1
            elif self.page >= self.page_number - 5:
                start_page = self.page_number - (self.plus * 2)
                end_page = self.page_number
            else:
                start_page = self.page - self.plus
                end_page = self.page + self.plus

        self.get_object.setlist(self.page_param, [1])
        page_str_list = ['<li><a href="?{}">首页</a></li>'.format(self.get_object.urlencode())]  # 首页
        if self.page > 1:
            self.get_object.setlist(self.page_param, [self.page-1])
            prev_page = '<li><a href="?{}">上一页</a></li>'.format(self.get_object.urlencode())  # 上一页
        else:
            self.get_object.setlist(self.page_param, [1])
            prev_page = '<li><a href="?{}">上一页</a></li>'.format(self.get_object.urlencode())
        page_str_list.append(prev_page)
        for i in range(start_page, end_page + 1):
            self.get_object.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.get_object.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.get_object.urlencode(), i)
            page_str_list.append(ele)
        if self.page < self.page_number:
            self.get_object.setlist(self.page_param, [self.page + 1])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.get_object.urlencode())  # 下一页
        else:
            self.get_object.setlist(self.page_param, [self.page_number])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.get_object.urlencode())
        page_str_list.append(next_page)
        self.get_object.setlist(self.page_param, [self.page_number])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.get_object.urlencode()))  # 尾页
        jump_str = """
               <li>
                   <form style="float: left; margin-left: -1px" method="get">
                       <input name="page"
                              style="position: relative; float: left; display: inline-block;
                              width: 80px; border-radius: 0" type="text" class="form-control" placeholder="页码">
                       <button style="border-radius: 0" class="btn btn-default" type="submit" >跳转</button>
                   </form>
               </li>
           """
        page_str_list.append(jump_str)
        page_string = mark_safe("".join(page_str_list))
        return page_string
