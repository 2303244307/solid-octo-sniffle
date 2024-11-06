from django.shortcuts import render, HttpResponse, redirect
from app01.models import Department
# Create your views here.


def test(request):
    return HttpResponse("测试服务")


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
    Department.objects.create(title=departtitle)
    return redirect("/depart/list")


def depart_delete(request):
    # 获取传输过来的nid
    nid = request.GET.get("nid")
    # 删除对应数据
    Department.objects.filter(id=nid).delete()
    # 页面重定向回到最开始界面
    return redirect("/depart/list")


def depart_edit(request, nid):
    """
    接受前端传来参数对部门表进行操作与编辑
    参数:
    返回:
    """
    ObjList = Department.objects.filter(id=nid).first()
    print(request.method)
    if request.method == "GET":
        return render(request, "depart_edit.html", {"ObjList":ObjList,})
    departname = request.POST.get("departname")
    Department.objects.filter(id=nid).update(title=departname)
    return redirect("/depart/list")


def depart_add(request):
    """ 进行添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    departtitle = request.POST.get("departname")
    print(departtitle)
    Department.objects.create(title=departtitle)
    return redirect("/depart/list")
