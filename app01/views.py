from django.core.validators import RegexValidator, ValidationError
from django.shortcuts import render, HttpResponse, redirect
from app01.models import Department, UserInfo, PrettyNum, UserAdmin
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
    return render(request, "user_edit.html", {"form": form, })


def User_delete(request, nid):
    # 通过传入nid用来删除对象
    UserInfo.objects.filter(id=nid).delete()
    # 页面重定向返回用户列表的位置
    return redirect("/User/list/")


def PrettyNum_list(request):
    # 获取表中所有数据
    prettyList = PrettyNum.objects.all()
    return render(request, "PrettyNum_list.html", {"prettyList":prettyList,} )

# 增加modeform表单对象用于使用
class PrettyNumModelForm(forms.ModelForm):
    # 此处可以添加对其它字段的校验
    # from django.core.validators import RegexValidator 需要导入这个模块对某个属性输入框进行校验
    # 验证方式1
    # mobile = forms.CharField(
    #     label="手机号码",
    #     # 此处如果存在多个正则进行判断的时候则可以通过逗号进行分割然后往下填写
    #     validators=[RegexValidator(r"^1[3-9]d{9}$", "手机号码格式校验错误")]
    # )
    class Meta:
        # 表明该表单类为那张表进行创建
        model = PrettyNum
        # 将需要可以输出输入框在此进行设置，表示获取选择的字段
        # fields = ["mobile", "price", "level", "status"]
        # 表示获取所有的字段
        fields = "__all__"
        # 还可以使用exclude用来排除那些字段，排除那些字段剩下的字段进行显示
        # exclude = []
        # 单独对上述列设置属性
        # widgets = {
        #     # 对表中元素单独进行设置
        #     # "mobile": forms.TextInput(attrs={"class": "form-control"})
        # }
            

    def __init__(self, *ages, **kwargs):
        super().__init__(*ages, **kwargs)
        for name, field in self.fields.items():
            # 通过遍历循环的形式来设置样式
            field.widget.attrs={"class": "form-control"}


    # 验证方式2的写法这种方法被称之为勾子方法首先需要定义一个方法然后方法名为clean_字段名，在其中再进行对字段校验
    def clean_mobile(self):
        # 在此处获取键盘输入内容
        text_mobile = self.cleaned_data["mobile"]
        if len(text_mobile) != 11:
            # 如果字段长度不等于11验证不通过，此处需要引入ValidationError函数from django.core.validators import RegexValidator, ValidationError
            raise ValidationError("手机号错误")
        # 验证通过则在此返回验证通过的内容
        return text_mobile

def PrettyNum_add(request):
    if request.method == "GET":
         # 实例化表单对象
        form = PrettyNumModelForm()
        return render(request, "PrettyNum_add.html", {"form": form,})
    # 获取post请求传输过来的表单数据
    form = PrettyNumModelForm(data=request.POST)
    # 进行数据验证
    if form.is_valid():
        # 将获取数据保存至表中
        form.save()
        # 界面重定向返回靓号管理界面
        return redirect("/PrettyNum/list/")
    # 如果数据验证错误重新回到界面，将错误信息传入
    return render(request, "PrettyNum_add.html", {"form": form,})

def PrettyNum_edit(request, nid):
    """ 用户编辑界面 """
    # 实例化表单对象
    rowobjects = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        edit_form = PrettyNumModelForm(instance=rowobjects)
        return render(request, "PrettyNum_edit.html", {"form": edit_form})
    # 将post请求数据传入，以及选择需要修改的数据
    edit_form = PrettyNumModelForm(instance=rowobjects, data=request.POST)
    # 进行数据验证
    if edit_form.is_valid():
        # 数据验证成功进行保存数据
        edit_form.save()
        # 域名重定向返回靓号列表
        return redirect("/PrettyNum/list/")
    # 如果数据验证未通过
    return render(request, "PrettyNum_edit.html", {"form": edit_form})



def PrettyNum_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/PrettyNum/list/")



def zxy_cc(request):
    # 此处添加爱心html
    return render(request, "index.html")

class UserAdminModelform(forms.ModelForm):
    class Meta:
        model = UserAdmin
        # 默认取出所有表字段数据用来进行添加
        fields = "__all__"
        # 字典方式对表单设计样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        # }
    def __init__(self, *args, **kwargs):
        # 此处调用父类的构造方法是因为需要通过父类的构造方法设置一些默认属性，再给属性中添加额外的属性，因为在此处相当于重写了构造方法
        super().__init__(*args, **kwargs)
        for name,filed in self.fields.items():
            filed.widget.attrs = {"class": "form-control"}
