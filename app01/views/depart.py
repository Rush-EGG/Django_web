from django.shortcuts import render, redirect, HttpResponse
from app01 import models

from app01.utils.pagination import Pagination


def depart_list(request):
    # 部门列表

    # 去数据库中找到所有的部门信息
    queryset = models.Department.objects.all()

    query_object = Pagination(request, queryset)
    context = {
        'queryset': query_object.page_queryset,
        'page_string': query_object.html()
    }

    return render(request, "depart_list.html",context)


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

