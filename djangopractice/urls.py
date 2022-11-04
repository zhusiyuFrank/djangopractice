"""djangopractice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import depart, manager, user, account, order, chart, upload, city

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/upload/', depart.depart_upload),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:uid>/edit/', user.user_edit),
    path('user/<int:uid>/delete/', user.user_delete),

    # 管理员
    path('admin/list/', manager.admin_list),
    path('admin/add/', manager.admin_add),
    path('admin/<int:aid>/edit/', manager.admin_edit),
    path('admin/<int:aid>/delete/', manager.admin_delete),
    path('admin/<int:aid>/reset/', manager.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),

    path('image/code/', account.image_code),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),

    # 文件上传
    path('upload/list/', upload.upload_list),

    # 城市
    path('city/list/', city.ciy_list),
    path('city/add/', city.city_add),
]
