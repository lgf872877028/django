from django.db import models


# Create your models here.
# 编辑部门表 只有标题和自带的id
class Department(models.Model):
    title = models.CharField(verbose_name="标题", max_length=32)

    # 让title 返回为srt字符串
    def __str__(self):
        return self.title


# 定义员工表 verbosen-name 可定义名称
class Userinfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="余额", max_digits=10, decimal_places=2, default=0)
    time = models.DateField(verbose_name="入职时间")
    # to 代表和哪个表连接  to_field 是和哪个字段连接 null是字段允许默认值为空 black填写的可以是空 on_delete  删除时的关联关系
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)
    gender_choices = ((1, "男"), (2, "女"),)
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


# 靓号表  choices  设置一个元组时 django会根据choices指定的元组实例找到对应的值
class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
