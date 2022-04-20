from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Create your views here.


def depart_list(request):
    # 部门列表

    # 去数据库中找到所有的部门信息
    queryset = models.Department.objects.all()

    return render(request, "depart_list.html", {"queryset": queryset})


def depart_add(request):
    # 添加部门
    if request.method == "GET":
        return render(request, "depart_add.html")

    # 获取用户提交的数据
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 回到显示页面
    return redirect("/depart/list")


def depart_delete(request):
    # 删除部门

    # 获取id
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 回到显示页面
    return redirect("/depart/list")
    # return HttpResponse("删除成功")


def depart_edit(request, nid):
    # 编辑部门

    if request.method == "GET":
        # 根据nid获取该行的数据
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id, row_object.title)

        return render(request, "depart_edit.html", {"row_object": row_object})

    # 得到用户提交的标题
    title = request.POST.get("title")
    # 根据id进行修改
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/depart/list")


def user_list(request):
    # 用户列表
    queryset = models.UserInfo.objects.all()

    return render(request, "user_list.html", {"queryset": queryset})


def user_add(request):
    # 添加用户

    if request.method == "GET":
        context = {
            'sex_choices': models.UserInfo.sex_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    sex_id = request.POST.get('sex')
    age = request.POST.get('age')
    ac = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    depart_id = request.POST.get('dp')

    models.UserInfo.objects.create(name=user, password=pwd, sex=sex_id,
                                   age=age, account=ac, create_time=ctime,
                                   depart_id=depart_id)

    return redirect("/user/list")


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password","sex", "age", "account", "create_time", "depart"]
        # 定义插件，以便于在前端显示想要的样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }

    # 重定义初始化方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环所有字段，给他们添加上想要的样式
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    # 基于ModelForm来添加用户
    if request.method == "GET":
        form = UserModelForm()

        return render(request, "user_model_form_add.html", {"form": form})

    # 用户通过Post提交数据，那么进行数据校验，如不允许字段为空
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 如果数据有效，那么保存到数据库
        # 到哪个数据库取决于form是实例化哪个对象
        form.save()
        return redirect("/user/list")
    else:
        # 校验失败，在页面上显示错误信息
        # print(form.errors)
        return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    # 编辑用户
    # 先得到修改的是哪一个用户
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # print(row_object.name)
        # 通过instance来确认现在编辑的是哪一名用户
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    # 如果用户是POST请求
    # 直接用ModelForm来拿到用户Post提交的信息，第二个参数是为了确定对哪一个用户进行更新
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        '''form.save()默认保存的是用户输入的内容
        如果想要它保存一些其他的字段
        可以这样来写：form.instance.字段名 = 值
        例如，来保存"修改时间"等一系列透明的信息
        '''
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list')


def pretty_list(request):
    # 靓号列表

    # 只为批量创建数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile='18158986469', price=100, level=2, status=2)

    # 查找1
    # q1 = models.PrettyNum.objects.filter(mobile="15957278805", id=2)
    # print(q1)
    # 查找2
    data_dict = {}
    # GET.get方法的第二个参数表示如果没有从GET方法中取到第一个参数，取的default值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 页码
    page = int(request.GET.get('page', 1))  # 当前显示的页码
    page_size = 10  # 每页显示10条数据
    start = (page - 1) * page_size
    end = page * page_size
    total = models.PrettyNum.objects.filter(**data_dict).count()  # 得到符合条件记录的个数
    # divmod()得到两个值，前者为除法结果，后者为取模结果
    total_page, div = divmod(total, page_size)
    if div:
        total_page += 1

    # 通过计算来使页面上显示的页码是当前页码的前plus页和后plus页
    plus = 5
    if total_page <= 2 * plus + 1:
        start_page = 1
        end_page = total_page
    else:
        if page <= plus:
            start_page = 1
            end_page = 2 * plus
        else:
            if (page + plus) > total_page:
                start_page = total_page - 2 * plus
                end_page = total_page
            else:
                start_page = page - plus
                end_page = page + plus

    page_str_list = []
    # 上一页
    prev = ''
    if page != 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    if prev != '':
        page_str_list.append(prev)
    # 构建页码表单
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)

        page_str_list.append(ele)
    # 下一页
    next = ''
    if page != total_page:
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    if next != '':
        page_str_list.append(next)
    # mark_safe()让浏览器信任该数据，并以html标签的形式显示到页面中
    page_string = mark_safe("".join(page_str_list))

    # 按照level来逆序排列
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start: end]

    return render(request, 'pretty_list.html',
                  {"queryset": queryset, "search_data": search_data,
                   "page_string": page_string})


class PrettyModelForm(forms.ModelForm):
    # 验证手机号格式方法1
    # mobile = forms.CharField(label="号码",
    #                          validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环所有字段，给他们添加上想要的样式
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证手机号格式方法2
    def clean_mobile(self):
        # 得到用户传入的数据
        mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=mobile).exists()

        if len(mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        elif exists:
            # 验证通过，返回用户输入的值
            raise ValidationError("手机号已存在")
        else:
            return mobile


def pretty_add(request):
    # 新建靓号
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    else:
        return render(request, 'pretty_add.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()

    return redirect('/pretty/list/')


class PrettyEditModelForm(forms.ModelForm):
    # 如果不允许对手机号进行修改，那就加上下面这一行
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环所有字段，给他们添加上想要的样式
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证手机号格式
    def clean_mobile(self):
        # 当前编辑这一行的主键 pk->primary key
        nid = self.instance.pk
        # 得到用户传入的手机号
        mobile = self.cleaned_data['mobile']
        # exclude()方法可以排除括号中的条件所筛选出来的记录
        exists = models.PrettyNum.objects.exclude(id=nid).filter(mobile=mobile).exists()

        if len(mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        elif exists:
            # 验证通过，返回用户输入的值
            raise ValidationError("手机号已存在")
        else:
            return mobile


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    # 如果用户是POST提交
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})