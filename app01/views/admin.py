from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm


def admin_list(request):
    # 管理员列表

    # 搜索功能
    data_dict = {}
    # GET.get方法的第二个参数表示如果没有从GET方法中取到第一个参数，取的default值
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去获取数据库中的记录
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页功能
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data
    }

    return render(request, 'admin_list.html', context)


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')  # 得到第一次输入的密码

        return md5(password)

    # 钩子函数
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        password = self.cleaned_data.get('password')  # 得到第一次输入的密码
        confirm = md5(self.cleaned_data.get('confirm_password'))  # 确认的密码
        if confirm != password:
            raise ValidationError("密码不一致！")

        # 返回的值会写入cleaned_data中，所以，对于clean_confirm_password函数返回的应该是confirm_password
        return confirm


def admin_add(request):
    # 添加管理员
    context = {
        'title': "新建管理员"
    }

    if request.method == 'GET':
        form = AdminModelForm()
        context['form'] = form

        return render(request, 'change.html', context)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 通过form.cleaned_data可以得到用户在本页面提交的所有信息
        form.save()
        return redirect('/admin/list/')

    context['form'] = form
    return render(request, 'change.html', context)


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


def admin_edit(request, nid):
    # 编辑管理员

    # 如果对象存在，则获取，如果不存在，只能拿到NULL
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': "对象不存在！"})

    title = "编辑管理员"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form": form, "title": title})


def admin_delete(request, nid):
    # 删除管理员
    models.Admin.objects.filter(id=nid).delete()

    return redirect('/admin/list/')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')  # 得到第一次输入的密码
        md5_pwd = md5(password)

        # 去数据库找一下原密码经md5加密之后的值和现密码经md5加密后的值一不一样
        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            # print("存在！")
            raise ValidationError("不能与之前的密码相同")

        return md5_pwd

    # 钩子函数
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        password = self.cleaned_data.get('password')  # 得到第一次输入的密码
        confirm = md5(self.cleaned_data.get('confirm_password'))  # 确认的密码
        if confirm != password:
            raise ValidationError("密码不一致！")

        # 返回的值会写入cleaned_data中，所以，对于clean_confirm_password函数返回的应该是confirm_password
        return confirm


def admin_reset(request, nid):
    # 重置密码
    # 如果对象存在，则获取，如果不存在，只能拿到NULL
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': "对象不存在！"})

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {'title': title, 'form': form})
