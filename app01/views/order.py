import json
import random
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        exclude = ['oid']


def order_list(request):
    # 显示订单列表
    form = OrderModelForm()

    return render(request, 'order_list.html', {'form': form})


@csrf_exempt
def order_add(request):
    # 新建订单
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 通过前端，没有传入订单的oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 保存到数据库
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
