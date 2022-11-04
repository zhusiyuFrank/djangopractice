from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator

from app01 import models
from app01.utils.pagination import Pagination


def user_list(request):
    # 搜索
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["name__contains"] = value
    userList = models.UserIndo.objects.filter(**data_dict)
    # 分页
    page_obj = Pagination(request, userList)

    context = {
        'userList': page_obj.page_queryset,
        'value': value,
        'page_string': page_obj.html()
    }
    return render(request, 'user_list.html', context)


class UserModelForm(forms.ModelForm):
    password = forms.CharField(
        label="密码",
        validators=[RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', '密码格式错误')]
    )

    class Meta:
        model = models.UserIndo
        fields = ["name", "password", "age", "salary", "create_time", "department", "gender"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "create_time":
                field.widget.attrs = {"class": "form-control", "placeholder": field.label,
                                      "autocomplete": "off"}  # 取消自动显示
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
    else:
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/list/')
        else:
            return render(request, 'user_add.html', {'form': form})


def user_edit(request, uid):
    row_obj = models.UserIndo.objects.filter(id=uid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {'form': form})
    else:
        form = UserModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect('/user/list/')
        else:
            return render(request, 'user_edit.html', {'form': form})


def user_delete(request, uid):
    models.UserIndo.objects.filter(id=uid).delete()
    return redirect("/user/list/")
