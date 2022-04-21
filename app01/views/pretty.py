from django.shortcuts import render, redirect, HttpResponse
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyModelForm, PrettyEditModelForm


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

    # 按照level来逆序排列
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "queryset": page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_string  # 数据的页码
    }

    return render(request, 'pretty_list.html', context)


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
