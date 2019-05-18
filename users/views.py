from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.core.paginator import *

from . import models
from goods import models as g_m
from order import models as o_m


from . import utils_tow


from django.db.models import Q
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from . import utils
from io import BytesIO
import re

import os

from django_redis import get_redis_connection


def email_exist(request):
    '''
    检测邮箱是否存在
    '''
    user_email = request.GET.get("email")
    count = models.Users.objects.filter(user_email=user_email).count()
    return JsonResponse({"count": count})


def name_exist(request):
    '''检测用户名是否已注册'''
    user_name = request.GET.get('user_name')
    count = models.Users.objects.filter(user_name=user_name).count()
    # 若count不为零，用户名已存在
    return JsonResponse({'count': count})


def send_verify(request):
    '''邮箱发送验证码'''

    code = utils.code()

    email = request.GET.get('email')
    subject = '生鲜超市用户注册'
    message = '【超市】验证码： %s 此验证码只用于校验邮箱，三分钟内有效' % code
    sender = settings.EMAIL_FROM
    # 收件人
    receiver = [email]
    try:
        send_mail(subject, message, sender, receiver)
        request.session['code'] = code
        # request.session.set_expiry(180)
        # 返回的验证码
        return JsonResponse({'code': code, 'news': 1})
    except:
        # 返回0，网络或者其它异常
        return JsonResponse(
            {'news': 0}
        )


def check_verify(request):
    '''检测验证码'''
    verify = request.GET.get("verify")

    if verify == request.session['code']:
        # msg==0 后端校验成功
        print("333333333")
        return JsonResponse({"news": 0})
    else:
        # msg==1 验证码错误
        return JsonResponse({"news": 1})


class Register(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, "users/register.html", {"title": "注册"})

    def post(self, request):
        post = request.POST
        user_email = post.get("email")
        user_name = post.get("user_name")
        user_pwd = post.get("pwd")
        print(user_email, user_name, user_pwd)
        e_re = r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'
        e_count = models.Users.objects.filter(user_email=user_email).count()
        if re.match(e_re, user_email) and e_count == 0:
            n_count = models.Users.objects.filter(user_name=user_name).count()
            if 2 <= len(user_name) <= 10 and n_count == 0:
                if 6 <= len(user_pwd) <= 16:

                    user = models.Users(user_name=user_name, user_pwd=user_pwd,
                                        user_email=user_email)
                    user.save()
                    return render(request, "users/login.html")
                else:
                    return render(request, "users/register.html", {"msg": "注册失败"})
            else:
                return render(request, "users/register.html", {"msg": "注册失败"})
        else:
            return render(request, "users/register.html", {"msg": "注册失败"})


class Login(View):
    '''登录处理函数'''
    def get(self, request):
        # 判断是否记住了用户名
        if 'user_value' in request.COOKIES:
            user_value = request.COOKIES.get("user_value")
            checked = 'checked'
        else:
            user_value = ''
            checked = ''
        return render(request, "users/login.html", {"user_value": user_value, "checked": checked, 'msg': '登录'})

    def post(self, request):
        post = request.POST
        user_value = post.get("username")
        print(user_value)
        user_pwd = post.get("pwd")
        n_user = models.Users.objects.filter(user_name=user_value)
        e_user = models.Users.objects.filter(user_email=user_value)
        if n_user.count() != 0:
            if n_user[0].user_pwd == user_pwd:
                # 记录用户的登陆状态
                request.session['loginUser'] = n_user[0].user_name
                # 跳转到首页
                response = redirect(reverse('goods:index'))
                # 判断是否需要记住用户名
                remember = post.get("remember")
                if remember == "on":
                    response.set_cookie("user_value", n_user[0].user_name, max_age=7*24*3600)
                else:
                    response.delete_cookie("user_value")
                return response
            else:
                return render(request, "users/login.html", {"info": "登陆失败", "msg": "登录"})
        elif e_user != 0:
            if e_user[0].user_pwd == user_pwd:
                # 记录用户的登陆状态
                request.session['loginUser'] = e_user[0].user_name
                # 跳转到首页
                response = redirect(reverse("goods:index"))
                # 判断是否需要记住用户名
                remember = post.get("remember")
                if remember == "on":
                    response.set_cookie("user_value", e_user[0].user_email, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie("user_value")
                return response

            else:
                return render(request, "users/login.html", {"info": "登陆失败", "msg": "登录"})
        else:
            return render(request, "users/login.html", {"info": "登陆失败", "msg": "登录"})


class Exit(View):
    """安全退出"""
    def get(self, request):
        request.session.flush()
        return redirect(reverse("goods:index"))


class UserInfo(View):
    '''用户信息中心'''
    def get(self, request):
        name = request.session['loginUser']
        user = models.Users.objects.get(user_name=name)
        goods_recently = g_m.Recently.objects.filter(user_id=user.id).order_by('-id')[0: 5]
        try:
            address = models.Address.objects.filter(user=user).order_by("-id")[0]

            # 历史浏览记录
            context = {"name": name, "info": "信息中心",
                       "address": address,
                       "goods_recently": goods_recently}

            return render(request, "users/user_center_info.html", context)
        except:
            return render(request, "users/user_center_info.html", {"name": name,
                                                                   "info": "信息中心",
                                                                   "goods_recently": goods_recently})


class UserOrder(View):
    '''用户订单中心'''
    def get(self, request, pindex):
        name = request.session['loginUser']
        user = models.Users.objects.get(user_name=name)

        orders = o_m.Order.objects.filter(user=user).order_by("-id")
        o_d = []
        for order in orders:
            order_detail = o_m.OrderDetail.objects.filter(order=order)
            order.order_detail = order_detail
            o_d.append(order)

        # 分页
        paginator = Paginator(orders, 2)
        try:
            page = paginator.page(int(pindex))
        except PageNotAnInteger:
            page = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面内容')
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return render(request, "users/user_center_order.html", {"name": name,
                                                                "info": "订单中心",
                                                                "o_d": o_d,
                                                                'page': page,
                                                                'paginator': paginator
                                                                })


class UserSite(View):
    '''用户地址中心'''
    def get(self, request):
        name = request.session['loginUser']
        print(name)
        user = models.Users.objects.get(user_name=name)
        try:
            address = models.Address.objects.filter(user=user).order_by("-id")[0]
            return render(request, "users/user_center_site.html", {"name": name, "address": address, "info": "地址中心"})
        except:
            return render(request, "users/user_center_site.html", {"name": name, "info": "地址中心"})

    def post(self, request):
        name = request.session['loginUser']
        user = models.Users.objects.get(user_name=name)
        post = request.POST

        try:
            address = models.Address.objects.get(user=user)
            address.addressee = post.get("addressee")
            address.direction = post.get("direction")
            address.zip_code = post.get("zip_code")
            address.addressee_contact = post.get("addressee_contact")
            address.save()
            return redirect(reverse("users:site"))
        except:
            addressee = post.get("addressee")
            direction = post.get("direction")
            zip_code = post.get("zip_code")
            addressee_contact = post.get("addressee_contact")

            address = models.Address(addressee=addressee,
                                     direction=direction,
                                     zip_code=zip_code,
                                     addressee_contact=addressee_contact,
                                     user=user)
            address.save()
            return redirect(reverse("users:site"))


def user_exist(request):
    user_name = request.GET.get("username")
    try:
        user = models.Users.objects.get(user_name=user_name)
        request.session['user_name'] = user.user_name
        return JsonResponse({"info": 0, "msg": ""})
    except:
        return JsonResponse({'info': 1, 'msg': '用户名不存在'})


# 验证码处理函数
def code(request):
    """
    :param request:
    :return: 返回一张验证码图片
    """
    img, code = utils_tow.create_code()
    # 首先需要将code保存到session中
    request.session['t_code'] = code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')
    return HttpResponse(file.getvalue(), "image/png")


# 检测验证码是否正确
def check_code(request):
    """

    :param request:
    :return:
    """
    code = request.GET.get("code")
    print(request.session['t_code'])
    print(code)
    if code == request.session['t_code']:
        return JsonResponse({'info': 0})
    else:
        return JsonResponse({'info': 1})


class ForgetPassword(View):

    def get(self, request):
        return render(request, "users/forgetPwd1.html")


def check_id(request):
    return render(request, "users/forgetPwd2.html")


def get_alert_pwd(request):
    return render(request, "users/forgetPwd3.html")


def post_alert_pwd(request):
    pwd = request.POST.get("pwd")
    user_name = request.session['user_name']
    try:
        user = models.Users.objects.get(user_name=user_name)
        user.user_pwd = pwd
        user.save()
        return JsonResponse({"news": 1})
    except:
        return JsonResponse({"news": 0})


def alert_ok(request):
    return render(request, "users/forgetPwd4.html")