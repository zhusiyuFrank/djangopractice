from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.pagination import Pagination


def admin_list(request):
    # 搜索
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["username__contains"] = value
    adminList = models.Admin.objects.filter(**data_dict)
    # 分页
    page_obj = Pagination(request, adminList)

    context = {
        'adminList': page_obj.page_queryset,
        'value': value,
        'page_string': page_obj.html()
    }
    return render(request, 'admin_list.html', context)


class AdminModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    password = forms.CharField(
        label="密码",
        validators=[RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', '密码格式错误')],
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致")
        return confirm_pwd


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'admin_add.html', {'form': form})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        else:
            return render(request, 'admin_add.html', {'form': form})


class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def admin_edit(request, aid):
    row_obj = models.Admin.objects.filter(id=aid).first()
    if not row_obj:  # 判断数据是否存在
        return redirect('/admin/list/')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'admin_edit.html', {'form': form})
    else:
        form = AdminEditModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        else:
            return render(request, 'admin_edit.html', {'form': form})


def admin_delete(request, aid):
    models.Admin.objects.filter(id=aid).delete()
    return redirect("/admin/list/")


class AdminResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    password = forms.CharField(
        label="密码",
        validators=[RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', '密码格式错误')],
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5(pwd)).exists()
        if exists:
            raise ValidationError("密码已存在")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致")
        return confirm_pwd


def admin_reset(request, aid):
    row_obj = models.Admin.objects.filter(id=aid).first()
    if not row_obj:  # 判断数据是否存在
        return redirect('/admin/list/')

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'admin_reset.html', {'form': form})
    else:
        form = AdminResetModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        else:
            return render(request, 'admin_reset.html', {'form': form})
