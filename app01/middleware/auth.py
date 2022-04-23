from django.middleware.common import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 首先要排除那些不需要登录就能访问的页面，包括登录界面和验证码生成界面
        # request.path_info 获取用户当前请求的url
        if request.path_info in ['/login/', '/image/code/']:
            return

        # 读取当前访问的用户的session信息
        # 如果能读到，说明用户已经登录
        info_dict = request.session.get('info')
        # 如果读到了，就让他进去
        if info_dict:
            # print(info_dict)
            return
        # 读不到，就引导到登录页面
        else:
            return redirect('/login/')
