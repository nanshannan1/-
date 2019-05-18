# coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def is_login(func):
    # 如果未登录则转到登录页面
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('loginUser'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect(reverse("users:login"))
            red.set_cookie('url', request.get_full_path())
            return red
    return login_fun
