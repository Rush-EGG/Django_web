import json
import random
import os
from datetime import datetime

from django import forms
from django.shortcuts import render, HttpResponse
from django.conf import settings

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.pagination import Pagination


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # print(request.POST)  # 请求体中的数据
    # print(request.FILES)  # 请求发过来的文件
    file_object = request.FILES.get('avatar')
    # print(file_object.name)  # 文件名

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse('...')


class UpForm(BootStrapForm):
    bootstrap_exclude_field = ['img']

    name = forms.CharField(label="姓名")
    age = forms.CharField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    if request.method == 'GET':
        form = UpForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        """
        读取内容 然后处理每个字段信息
            读取图片内容，写入到文件夹中并获取文件路径
            将图片的路径写入到数据库中
        """
        image_object = form.cleaned_data.get('img')

        media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)

        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )

        return HttpResponse("上传成功")

    return render(request, 'upload_form.html', {'form': form, 'title': title})


class UpModalForm(BootStrapModelForm):
    bootstrap_exclude_field = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def upload_form_modal(request):
    # 上传文件和数据（ModalForm方法）
    title = "ModalForm上传"
    if request.method == 'GET':
        form = UpModalForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 自动保存文件，且将字段+上传路径写入到数据库
        form.save()

        return HttpResponse("上传成功")

    return render(request, 'upload_form.html', {'form': form, 'title': title})
