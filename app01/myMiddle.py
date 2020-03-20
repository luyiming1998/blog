from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re


class MyMiddleAware1(MiddlewareMixin):
    def process_request(self, request):
        user = request.session.get("userinfo")
        if not user:  # 如果用户未登录,访问如下链接跳转至登录页面
            perssion_list = [
                "/update_user/",
                "/upload_avatar/",
                "/pub_article/",
                "/show_my_article/",
                "/update_article/",
                "/del_article/",
                "/post_comment/"
            ]
            path = re.sub(r'\d+', "", request.path)
            # print(path)
            if path in perssion_list:
                return redirect("/login.html")
        # print(request.path)
