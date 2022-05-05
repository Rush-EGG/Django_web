from django.utils.safestring import mark_safe
import copy
"""
如果以后想要使用分页组件，那么要做以下几件事情
1.根据情况筛选想要的数据，存放在queryset中
2.实例化分页对象
在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成页码
        }
        return render(request, '***.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param='page', plus=5):
        page = request.GET.get(page_param, '1')

        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 为这个对象添加一些元素
        self.page = page
        self.page_size = page_size
        self.plus = plus
        self.page_param = page_param

        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 已经分完页的数据
        self.page_queryset = queryset[self.start: self.end]

        total = queryset.count()  # 得到符合条件记录的个数
        # divmod()得到两个值，前者为除法结果，后者为取模结果
        total_page, div = divmod(total, page_size)
        if div:
            total_page += 1
        self.total_page = total_page

        # 为保证能同时筛选和分页
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

    def html(self):
        # 通过计算来使页面上显示的页码是当前页码的前plus页和后plus页
        if self.total_page <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                if (self.page + self.plus) > self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []
        # 上一页
        prev = ''
        if self.page != 1:
            # 在query_dict这个字典中添加字段：'page': self.page-1
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        if prev != '':
            page_str_list.append(prev)
        # 构建页码表单
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            page_str_list.append(ele)
        # 下一页
        next = ''
        if self.page != self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        if next != '':
            page_str_list.append(next)

        # 分页组件
        search_string = """
            <li>
                <form style="float: left; margin-left: -1px" method="GET">
                    <input name="page"
                           style="position: relative; float: left; display: inline-block; width: 80px; border-radius: 0"
                           class="form-control" type="text" placeholder="页码">
                    <button class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
        """
        page_str_list.append(search_string)

        # mark_safe()让浏览器信任该数据，并以html标签的形式显示到页面中
        page_string = mark_safe("".join(page_str_list))

        return page_string
