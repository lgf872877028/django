import requests
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Create your views here.
# 定义模版
def layout(request):
    return render(request, 'layout.html')


# 定义返还给部门列表 并传入queryset queeryset的值时部门表中所有的数据 数据类型时列表
def depart_list(request):
    # queryset类型  是一个列表
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


# 如果时get访问 没有post提交的话 返回用户添加页面 在post表单提交后 根据提交的标题 title 使用——
# models。表名。objects。create（表中列 = 实例化对象）然后返回重定向的部门列表

def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list")


# 删除用户  先遍历用户列表传回的que 得到表中所有数据后生成对应id的的编辑按钮和删除按钮 然后通过get方式将id拼接到url上传入views
# nid 等于传回的id  从数据库中用filter找到id对应的行  将他删除 然后重定向回部门列表
def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")


# 编辑部门列表 用上述删除同样方法回传id 找到对应行后返还给编辑页面 并把他的要编辑的行的数据回传
# 在编辑完成后得到post请求 将标题使用filerr找到对应id后 .update更新新的title 然后重定向回部门列表

def depart_edit(request, nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")


# 定义modelsforms样式的class
#
class UserinfoForm(forms.ModelForm):
    #   重写name 样式 让modelsforms中的默认的验证方式改变为最小为3
    name = forms.CharField(min_length=3, label="用户名")

    # class meta代表这对哪个表进行操作 model = 操作的表 fields='__all__'表明找到表中所有的列
    class Meta:
        model = models.Userinfo
        fields = '__all__'

    # 重写方法 让models生成的所有input框添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的表单中的字典 字典的name是单纯的字符串 对应的值field是表中的元组 元组中是字段名称  第二个是字段对象
        # 因为self。fields。items是一个迭代器 所以遍历时必须使用两个值 即使name在后续不需要使用也不能省略
        # field字段对象中包含了生成input框中的所有属性和方法

        for name, field in self.fields.items():
            # if name == "password":
            #     continue

            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
        mobile_validators = [RegexValidator(r'^\d{11}$', message='手机号必须是 11 位数字')]

    def clean_mobile(self):
        """ 确保 mobile 字段唯一 """
        mobile = self.cleaned_data['mobile']
        if models.PrettyNum.objects.filter(mobile=mobile).exists():
            raise ValidationError('手机号已存在')
        return mobile


# 设置用户列表 form实例化 class类  并通过循环field.label_tag 得到所有userinfo表中的行设置的中文名
# q得到数据表中所有数据并显示到页面
def user_list(request):
    form = UserinfoForm()
    q = models.Userinfo.objects.all()

    return render(request, 'user_list.html', {'form': form, 'q': q})


# 设置用户添加功能 get直接打开返回用户添加页面并传入from from时modelforms中生成的所有input框
# 提交表单后返回访问方式为post则验证 正确输入则进行保存然后重定向回用户列表 错误输入则提示错误继续返还当前的添加页面
# 验证功能的默认验证只验证是否为空 别的功能需要在设置modelforms的重写方法
def user_add(request):
    if request.method == "GET":
        form = UserinfoForm()
        return render(request, 'user_add.html', {'form': form})

    form = UserinfoForm(data=request.POST)

    if form.is_valid():
        form.save()

        return redirect('/user/list')

    return render(request, 'user_add.html', {'form': form})


# 设置用户编辑 如果时get直接返还 用户编辑页面 先通过传回的nid得到需要编辑的id 然后把相应的数据传回给编辑页面
# form = userinfoform中 实例化了 instance=row 让打开编辑页面时数据显示在输入框中 做到默认值的效果
# 提交时通过实例化设置data 等于传回方式post 然后把默
def user_edit(request, nid):
    row = models.Userinfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserinfoForm(instance=row)
        return render(request, 'user_edit.html', {'form': form})
    # 先通过row找到需要保存的数据在哪一行 然后验证时post提交的表单的话将数据保存进这一行 不传在form中传入row的话话会导致数据得不到更新 反而是增加

    form = UserinfoForm(data=request.POST, instance=row)
    if form.is_valid():
        # userinfo = form.save(commit=False)
        # userinfo.account = 0
        # userinfo.save()
        form.save()

        return redirect('/user/list')
    return render(request, 'user_edit.html', {'form': form})


# 从get请求中获取get 然后在m通过查找。delete删除
def user_delect(request):
    nid = request.GET.get('nid')
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


class prettyinfo(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = '__all__'

    #     在类中给后续添加框添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的表单中的字典 字典的name是单纯的字符串 对应的值field是表中的元组 元组中是字段名称  第二个是字段对象
        # 因为self。fields。items是一个迭代器 所以遍历时必须使用两个值 即使name在后续不需要使用也不能省略
        # field字段对象中包含了生成input框中的所有属性和方法

        for name, field in self.fields.items():
            # if name == "password":
            #     continue

            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

        mobile_validators = [RegexValidator(r'^\d{11}$', message='手机号必须是 11 位数字')]
        self.fields['mobile'].validators.extend(mobile_validators)

    def clean_mobile(self):
        """ 确保 mobile 字段唯一 """
        mobile = self.cleaned_data['mobile']

        if models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=mobile).exists():
            raise ValidationError('手机号已存在')
        return mobile


def pretty_list(request):
    m = prettyinfo()
    data = request.GET.get('q')


    if data:
        form = models.PrettyNum.objects.filter(mobile__contains=data).order_by("-level")
        return render(request, 'pretty_list.html', {'m': m, 'form': form, 'data': data})

    form=models.PrettyNum.objects.all().order_by("-level")
    return render(request, 'pretty_list.html', {'m': m, 'form': form,'data':data})


def pretty_add(request):
    if request.method == "GET":
        form = prettyinfo()
        return render(request, 'pretty_add.html', {'form': form})

    form = prettyinfo(data=request.POST)

    if form.is_valid():
        form.save()

        return redirect('/pretty/list')

    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    # 获取前端传入的数据
    row = models.PrettyNum.objects.filter(id=nid).exclude().first()
    # get 方式 则直接返回页面
    if request.method == "GET":
        form = prettyinfo(instance=row)
        return render(request, 'pretty_edit.html', {'form': form})
    # 先通过row找到需要保存的数据在哪一行 然后验证时post提交的表单的话将数据保存进这一行 不传在form中传入row的话话会导致数据得不到更新 反而是增加

    form = prettyinfo(data=request.POST, instance=row)
    if form.is_valid():
        # userinfo = form.save(commit=False)
        # userinfo.account = 0
        # userinfo.save()
        form.save()

        return redirect('/pretty/list')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request):
    nid = request.GET.get('nid')
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')
