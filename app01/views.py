from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms

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