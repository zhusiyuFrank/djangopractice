import random

from django.shortcuts import render
from django.http import JsonResponse

from app01 import models


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    """柱状图数据"""
    query_set = models.Admin.objects.all()
    legend = []
    series_list = []
    for i in query_set:
        legend.append(i.username)
        series_list.append({
            'name': i.username,
            'type': 'bar',
            'data': [random.randint(10, 99), random.randint(10, 99), random.randint(10, 99),
                     random.randint(10, 99), random.randint(10, 99), random.randint(10, 99)]
        })
    xAxis = ["1月", "2月", "3月", "4月", "5月", "6月"]
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': xAxis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    data_list = []
    query_set = models.Department.objects.all()
    for i in query_set:
        value = random.randint(10, 99)
        data_list.append({'value': value, 'name': i.title})
    result = {
        'status': True,
        'data': data_list,
    }
    return JsonResponse(result)


def chart_line(request):
    query_set = models.Department.objects.all()
    legend = []
    series_list = []
    for i in query_set:
        legend.append(i.title)
        series_list.append({
            'name': i.title,
            'type': 'line',
            'stack': 'Total',
            'data': [random.randint(100, 999), random.randint(100, 999), random.randint(100, 999),
                     random.randint(100, 999), random.randint(100, 999), random.randint(100, 999),]
        })
    xAxis = ["1月", "2月", "3月", "4月", "5月", "6月"]
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': xAxis,
        }
    }
    return JsonResponse(result)
