from django.shortcuts import render, HttpResponse, redirect
from app01.models import Department, UserInfo
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
    return render(request, "User_List.html", {"UserList": UserList, })


def User_add(request):
    # 获取部门数据传入
    departList = Department.objects.all()
    # 判断此次请求是什么请求如果是get请求默认加载页面
    if request.method == "GET":
        return render(request, "User_add.html", {"departList":departList,})
    # 获取前端传出值
    UserName = request.POST.get("UserName")
    passwd = request.POST.get("passwd")
    age = request.POST.get("age")
    account = request.POST.get("account")
    depart_id = request.POST.get("depart")
    gender = request.POST.get("gender")
    # 进行表操作插入表数据
    UserInfo.objects.create(name=UserName, password=passwd,
                            age=age, account=account, depart_id=depart_id, gender=gender)
    # 进行页面重定向回到用户列表界面
    return redirect("/User/list/")
