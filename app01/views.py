from django.shortcuts import render, HttpResponse, redirect
from app01.models import Department, UserInfo
from django import forms


# Create your views here.


def yunge(request):
    pass


def depart_list(request):
    """ 部门列表 """
    # 去数据库中获取部门列表数据获取所有的部门列表
    DepartList = Department.objects.all()
    return render(request, "depart_list.html", {"DepartList": DepartList, })


def adddepart(request):
    """ 进行添加部门 """
    if request.method == "GET":
        return render(request, "adddepart.html")
    departtitle = request.POST.get("departname")
    print(departtitle)
    Department.objects.create(title=departtitle)
    return redirect("/depart/list")


def depart_delete(request):
    # 获取传输过来的nid
    nid = request.GET.get("nid")
    # 删除对应数据
    Department.objects.filter(id=nid).delete()
    # 页面重定向回到最开始界面
    return redirect("/depart/listpro")


def depart_edit(request, nid):
    """
    接受前端传来参数对部门表进行操作与编辑
    参数:
    返回:
    """
    ObjList = Department.objects.filter(id=nid).first()
    print(request.method)
    if request.method == "GET":
        return render(request, "depart_edit.html", {"ObjList": ObjList, })
    departname = request.POST.get("departname")
    Department.objects.filter(id=nid).update(title=departname)
    return redirect("/depart/list")


def depart_listpro(request):
    """ 部门列表 模板继承升级版本"""
    # 去数据库中获取部门列表数据获取所有的部门列表
    DepartList = Department.objects.all()
    return render(request, "depart_list1.html", {"DepartList": DepartList, })


def depart_addpro(request):
    """ 进行添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    departtitle = request.POST.get("departname")
    print(departtitle)
    Department.objects.create(title=departtitle)
    return redirect("/depart/listpro")


def depart_editpro(request, nid):
    """
    接受前端传来参数对部门表进行操作与编辑
    参数:
    返回:
    """
    ObjList = Department.objects.filter(id=nid).first()
    print(request.method)
    if request.method == "GET":
        return render(request, "depart_editpro.html", {"ObjList": ObjList, })
    departname = request.POST.get("departname")
    Department.objects.filter(id=nid).update(title=departname)
    return redirect("/depart/listpro")


def User_list(request):
    # 获取用户表queryset对象
    UserList = UserInfo.objects.all()
    # 使用python语法获取需要的数据
    for obj in UserList:
        # 获取其中各个字段的参数
        print(obj.name, obj.password, obj.age, obj.account, obj.depart.title,
              obj.get_gender_display(), obj.create_date.strftime("%Y-%m-%d"))
        # , obj.create_date.strftime("%Y-%m-%d") 将日期格式数据进行调整与使用
        # obj.depart相当于获取对应的Department对象再通过这个对象通过.方式获取对应的属性
    return render(request, "User_List.html", {"UserList": UserList, })


def User_add(request):
    # 添加用户的原始方式
    # 获取部门数据传入
    departList = Department.objects.all()
    # 判断此次请求是什么请求如果是get请求默认加载页面
    if request.method == "GET":
        return render(request, "User_add.html", {"departList": departList, })
    # 获取前端传出值
    UserName = request.POST.get("UserName")
    passwd = request.POST.get("passwd")
    age = request.POST.get("age")
    account = request.POST.get("account")
    depart_id = request.POST.get("depart")
    gender = request.POST.get("gender")
    create_date = request.POST.get("ctime")
    # 进行表操作插入表数据
    UserInfo.objects.create(name=UserName, password=passwd,
                            age=age, account=account, depart_id=depart_id, gender=gender, create_date=create_date)
    # 进行页面重定向回到用户列表界面
    return redirect("/User/list/")


class UserModelForm(forms.ModelForm):
    # 在此处还可以给字段进行添加其它的校验, 同时也可以自定义字段名在此进行使用
    # min_length设置最短长度 max_length设置最长长度  label设置字段描述
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        # 让model指向模型方便进行解析
        model = UserInfo
        # 可以有input属性的进行放出
        fields = ["name", "password", "age", "account",
                  "depart", "gender", "create_date"]
        # 在此可以定义出现的列的样式属性
        # widgets = {
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "password":
                field.widget.attrs = {"class": "form-control"}
            else:
                # 给密码单独设置加密
                field.widget = forms.PasswordInput(
                    attrs={"class": "form-control"})


def user_model_form_add(request):
    if request.method == "GET":
        # 实例化form对象 需要在类中新建一个UserModelForm
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form, })
    # 提取用户提交的post数据
    form = UserModelForm(data=request.POST)
    # 对用户提交数据进行校验
    if form.is_valid():
        # 输出获取来的提交数据
        print(form.cleaned_data)
        # {'name': '张帅帅', 'password': '11111', 'age': 12, 'account': Decimal('22'), 'depart': <Department: 院办>, 'gender': 1, 'create_date': datetime.datetime(2024, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))}
        # django ModeFrom支持另一种将数据保存的写法
        # 将数据进行存储
        form.save()
        return redirect("/User/list/")
    # 输出错误数据
    print(form.errors)
    return render(request, "user_model_form_add.html", {"form": form, })


def User_edit(request, nid):
    # 通过传入nid获取数据对象
    RowObject = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 通过nid获取数据对象
        # 实例化form对象 同时将需要设置默认值的对象传进去
        form = UserModelForm(instance=RowObject)
        # 将设置好存在各个属性的对象进行传入到前端
        return render(request, "user_edit.html", {"form": form, })
    # 提取用户提交的post数据，并通过数据对象表达此次为修改操作
    form = UserModelForm(data=request.POST, instance=RowObject)
    # 对用户提交数据进行校验
    if form.is_valid():
        # 输出获取来的提交数据
        print(form.cleaned_data)
        # {'name': '张帅帅', 'password': '11111', 'age': 12, 'account': Decimal('22'), 'depart': <Department: 院办>, 'gender': 1, 'create_date': datetime.datetime(2024, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))}
        # django ModeFrom支持另一种将数据保存的写法
        # 将数据进行存储此
        # 此处进行保存是用户在前端界面输入的值，如果需要需要在代码中写值可以是像操作时间一般就是直接后台进行写入的
        # form.instance.字段名="某值"
        form.save()
        return redirect("/User/list/")
    # 输出错误数据
    print(form.errors)
    return render(request, f"User/{nid}/edit/", {"form": form, })


def User_delete(request, nid):
    # 通过传入nid用来删除对象
    UserInfo.objects.filter(id=nid).delete()
    # 页面重定向返回用户列表的位置
    return redirect("/User/list/")


def zxy_cc(request):
    return render(request, "index.html")
