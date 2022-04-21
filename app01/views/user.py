from django.shortcuts import render, redirect, HttpResponse
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    # 用户列表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset)
    context = {'queryset': page_object.page_queryset,
               'page_string': page_object.html()}

    return render(request, "user_list.html", context)


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
        '''
        form.save()默认保存的是用户输入的内容
        如果想要它保存一些其他的字段
        可以这样来写：form.instance.字段名 = 值
        例如，来保存"修改时间"等一系列透明的信息
        '''
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list')

