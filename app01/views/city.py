from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination


def ciy_list(request):
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["name__contains"] = value
    cityList = models.City.objects.filter(**data_dict)

    page_obj = Pagination(request, cityList)

    context = {
        'cityList': page_obj.page_queryset,
        'value': value,
        'page_string': page_obj.html()
    }
    return render(request, 'city_list.html', context)


class CityModelForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'img':
                continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def city_add(request):
    if request.method == 'GET':
        form = CityModelForm()
        return render(request, 'city_add.html', {'form': form})
    else:
        form = CityModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/city/list/')
        else:
            return render(request, 'city_add.html', {'form': form})
