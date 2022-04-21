from app01 import models
from django import forms
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=2, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password","sex", "age", "account", "create_time", "depart"]
        # 定义插件，以便于在前端显示想要的样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }


class PrettyModelForm(BootStrapModelForm):
    # 验证手机号格式方法1
    # mobile = forms.CharField(label="号码",
    #                          validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        fields = "__all__"

    # 验证手机号格式方法2
    def clean_mobile(self):
        # 得到用户传入的数据
        mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=mobile).exists()

        if len(mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        elif exists:
            # 验证通过，返回用户输入的值
            raise ValidationError("手机号已存在")
        else:
            return mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 如果不允许对手机号进行修改，那就加上下面这一行
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"

    # 验证手机号格式
    def clean_mobile(self):
        # 当前编辑这一行的主键 pk->primary key
        nid = self.instance.pk
        # 得到用户传入的手机号
        mobile = self.cleaned_data['mobile']
        # exclude()方法可以排除括号中的条件所筛选出来的记录
        exists = models.PrettyNum.objects.exclude(id=nid).filter(mobile=mobile).exists()

        if len(mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        elif exists:
            # 验证通过，返回用户输入的值
            raise ValidationError("手机号已存在")
        else:
            return mobile
