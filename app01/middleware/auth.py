from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect


class M1(MiddlewareMixin):
    def process_request(self, request):
        # 如果当前访问的URL是/login/，返回none继续向后走
        if request.path_info in ['/login/', '/image/code/']:
            return
        # 读取用户session信息，不存在回登录界面，存在则可以访问
        info = request.session.get('info')
        if not info:
            return redirect('/login/')
        else:
            return
