from io import BytesIO

from django import forms
from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.code import check_code


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():

            # 先做验证码校验（clean_data里有code，数据库里没有。先把code pop出来才能进行数据库查找)
            user_input_code = form.cleaned_data.pop('code')
            code = request.session.get('image_code', "")
            if code.upper() != user_input_code.upper():
                form.add_error("code", "验证码不一致")
                return render(request, 'login.html', {'form': form})

            # 验证用户名密码与数据库的数据是否匹配
            admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
            if not admin_obj:
                form.add_error("password", "用户名或密码错误")
                return render(request, 'login.html', {'form': form})
            else:
                request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.username}
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect("/admin/list/")
        else:
            return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    # 生成图片
    img, code_string = check_code()
    # 写入到session
    request.session['image_code'] = code_string
    # 60秒超时
    request.session.set_expiry(60)
    # 写入内存文件
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
