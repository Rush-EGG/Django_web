from django.db import models

# Create your models here.


class Department(models.Model):
    # 部门表
    title = models.CharField(verbose_name='标题', max_length=32)


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
    create_time = models.DateTimeField(verbose_name='入职时间')

    '''
    使depart与部门表约束
    to决定了与哪一张表有关联，to_field决定与这张表中的哪一列有关联
    Django有个机制，凡是这种与其他表有约束的列，均会在定义的列名后加上"_id"
    '''
    # 如果需要级联删除，那么写上on_delete=models.CASCADE
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE)
    # 如果置空，那么首先这一列需要满足为可空
    # depart = models.ForeignKey(to='Department', to_field='id',null=True, blank=True, on_delete=models.SET_NULL)
