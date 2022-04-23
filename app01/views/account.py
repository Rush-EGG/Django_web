from io import BytesIO

from django import forms
from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        return md5(pwd)


def login(request):
    # 用户登录
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，得到用户名和密码和验证码
        # form.cleaned_data

        # 验证码的校验
        # 用pop的原因是因为去数据库校验的时候只拿用户名和密码，与验证码无关
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')

        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 验证码对了，拿着用户名和密码去数据库校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 主动在form中添加错误信息，并传到前端
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码输入正确
        # 网站要生成一个随机字符串，写入到用户浏览器的cookie中，并写入到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    # 注销
    request.session.clear()

    return redirect('/login')


def image_code(request):
    # 生成验证码

    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # 得到生成的验证码文本
    print(code_string)

    # 写入到session中，以便于后续获取并进行校验
    request.session['image_code'] = code_string
    # 设置一个60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
