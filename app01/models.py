from django.db import models

# Create your models here.


class UserAdmin(models.Model):
    """ 管理员表 """
    name = models.CharField(max_length=22)
    password = models.CharField(max_length=33)
    age = models.IntegerField()


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=22)   # verbose_name="标题"这是相当于注解字段的含义


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    # max_digits是数字的长度 decimal_places是保留多少位小数
    account = models.DecimalField(verbose_name="账户", max_digits=10, decimal_places=2)
    # 用户表存储部门表的话一般存储id而不是存储名称，这样可以节省数据库空间(数据库范式),还需要给部门id增加约束相当于存在此表的id要在部门表中存在
    # 约束的写法
    # to表示与那张表存在关联 to_field表示关联的那张表的什么字段
    # 表中定义字段为depart 但django会自动生成对应的数据列，列名为depart_id
    # 如果部门表中对应内容被删除这条内容跟着一起删除被称之为级联删除
    # 级联删除写法
    depart = models.ForeignKey(to=Department, to_field="id", on_delete=models.CASCADE)
    # 如果部门表被删除，用户对应的改字段置为空
    # depart = models.ForeignKey(to=Department, to_field="id",null=True, blank=True, on_delete=models.SET_NULL)

    # 枚举数据类型
    gender_choices = ((1,"男"),(2,"女"))
    # 在django中增加约束1男2女
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    create_date = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")