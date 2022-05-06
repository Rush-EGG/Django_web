import json
import random
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


def chart_list(request):
    # 数据统计页面
    return render(request, 'chart_list.html')


def chart_bar(request):
    # 构造柱状图数据
    # 这里是写死了 但也可以从数据库中去获取
    legend = ["销量", "成本"]
    data_list = [
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '成本',
            'type': 'bar',
            'data': [10, 15, 3, 100, 11, 2]
        }
    ]
    x_list = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'data_list': data_list,
            'x_list': x_list
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    # 构造饼图数据
    db_data_list = [
        {'value': 2048, 'name': 'IT部门'},
        {'value': 1735, 'name': '运营'},
        {'value': 580, 'name': '新媒体'},
    ]

    result = {
        'status': True,
        'data': db_data_list
    }
    return JsonResponse(result)
