import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


def task_list(request):
    # 任务管理
    form = TaskModelForm()
    return render(request, 'task_list.html', {'form': form})


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)

    data_dict = {'status': True, 'data': [11, 22, 33, 44]}
    # 方式1
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)

    # 方式2
    # return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    print(request.POST)
    # 对用户发送过来的信息做校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()

        data_dict = {'status': True}
        json_string = json.dumps(data_dict)

        return HttpResponse(json_string)

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
