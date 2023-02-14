from django.shortcuts import render, redirect
from app01 import models
from django import forms


# Create your views here.
def layout(request):
    return render(request, 'layout.html')


def depart_list(request):
    # queryset类型  是一个列表
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list")


def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")


def depart_edit(request, nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list")


class UserinfoForm(forms.ModelForm):
    #   重写name 样式
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.Userinfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_list(request):
    form = UserinfoForm()
    q = models.Userinfo.objects.all()

    return render(request, 'user_list.html', {'form': form, 'q': q})


def user_add(request):
    if request.method == "GET":
        form = UserinfoForm()
        return render(request, 'user_add.html', {'form': form})

    form = UserinfoForm(data=request.POST)

    if form.is_valid():
        form.save()

        return redirect('/user/list')

    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    if request.method == "GET":
        row = models.Userinfo.objects.filter(id=nid).first()
        form = UserinfoForm(instance=row)
        return render(request, 'user_edit.html', {'form': form})

    row = models.Userinfo.objects.filter(id=nid).first()
    form = UserinfoForm(data=request.POST, instance=row)
    if form.is_valid():
        # userinfo = form.save(commit=False)
        # userinfo.account = 0
        # userinfo.save()
        form.save()

        return redirect('/user/list')
    return render(request, 'user_edit.html', {'form': form})
def user_delect(request ):
    nid = request.GET.get('nid')

    models.Userinfo.objects.filter(id=nid).delete()
    return redirect('/user/list')

