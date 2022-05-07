from django.db import models


# Create your models here.

class Admin(models.Model):
    # 管理员表
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    # 部门表
    title = models.CharField(verbose_name='标题', max_length=32)

    # 定制了print(Department)时显示的内容是部门的名称
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    # 员工表
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)

    # Django中有的约束
    sex_choices = (
        (1, "男"),
        (2, "女")
    )
    sex = models.SmallIntegerField(verbose_name='性别', choices=sex_choices)

    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')

    '''
    使depart与部门表约束
    to决定了与哪一张表有关联，to_field决定与这张表中的哪一列有关联
    Django有个机制，凡是这种与其他表有约束的列，均会在定义的列名后加上"_id"
    '''
    # 如果需要级联删除，那么写上on_delete=models.CASCADE
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE, verbose_name="部门")
    # 如果置空，那么首先这一列需要满足为可空
    # depart = models.ForeignKey(to='Department', to_field='id',null=True, blank=True, on_delete=models.SET_NULL)


class PrettyNum(models.Model):
    # 靓号表
    mobile = models.CharField(verbose_name="手机号", max_length=11)
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
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    # 任务
    level_choices = {
        (1, "紧急"),
        (2, "常规"),
        (3, "临时"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息", max_length=100)
    user = models.ForeignKey(verbose_name="负责人", to='Admin', on_delete=models.CASCADE)


class Order(models.Model):
    # 工单
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = {
        (1, "待支付"),
        (2, "已支付")
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    admin = models.ForeignKey(verbose_name="管理员", to='Admin', on_delete=models.CASCADE)


class Boss(models.Model):
    # 老板
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    # 城市
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    # 本质上FileField也是CharField，多了一个django内部帮你做保存的功能
    # upload_to会帮你将文件保存到media文件夹下某一文件夹
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')
