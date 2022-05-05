import json
import random
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        # 排除oid和管理员id
        exclude = ['oid', 'admin']


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    # 显示订单列表
    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    # 新建订单
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 通过前端，没有传入订单的oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 固定设置，即当前登录的是谁，这个订单就是谁创建的
        form.instance.admin_id = request.session['info']['id']
        # 保存到数据库
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
