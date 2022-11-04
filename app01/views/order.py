import random
from datetime import datetime

from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid", "admin"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def order_list(request):
    # 搜索
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["title__contains"] = value
    orderList = models.Order.objects.filter(**data_dict)
    # 分页
    page_obj = Pagination(request, orderList)

    form = OrderModelForm()

    context = {
        'form': form,
        'orderList': page_obj.page_queryset,
        'value': value,
        'page_string': page_obj.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单 Ajax请求"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 生成订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 获取登录的管理员id
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):
    o_id = request.GET.get("oid")
    models.Order.objects.filter(id=o_id).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    oid = request.GET.get("oid")
    obj = models.Order.objects.filter(id=oid).values("title", "price", "status").first()
    if not obj:
        return JsonResponse({'status': False, 'error': "数据不存在"})
    result = {
        'status': True,
        'data': obj,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    oid = request.GET.get("oid")
    row_obj = models.Order.objects.filter(id=oid).first()
    # 如果数据不存在
    if not row_obj:
        return JsonResponse({'status': False, 'tip': "数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
