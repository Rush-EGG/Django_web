import json
import random
import os
from datetime import datetime

from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.pagination import Pagination


def city_list(request):
    queryset = models.City.objects.all()

    return render(request, 'city_list.html', {'queryset': queryset})


class UpModalForm(BootStrapModelForm):
    bootstrap_exclude_field = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def city_add(request):
    title = "新建城市"
    if request.method == 'GET':
        form = UpModalForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()

        return redirect('/city/list/')

    return render(request, 'upload_form.html', {'form': form, 'title': title})
