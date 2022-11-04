from django.db import models


# Create your models here.
class Admin(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门", max_length=32)

    def __str__(self):
        return self.title


class UserIndo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="工资", default=0, max_digits=10, decimal_places=2)
    create_time = models.DateField(verbose_name="入职时间")
    department = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)  # 级联删除
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class City(models.Model):
    name = models.CharField(verbose_name="城市名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to="city/")
