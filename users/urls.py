# coding:utf-8
from django.conf.urls import url
from . import views
from .decorators import is_login

urlpatterns = [
    # 注册函数
    url(r"^register/$", views.Register.as_view(), name="register"),
    # 校验邮箱
    url(r"^email_exist/$", views.email_exist, name="email_exist"),
    # 校验用户名
    url(r"^name_exist/$", views.name_exist, name="name_exist"),
    # 发送验证码
    url(r'^send_verify/$', views.send_verify, name="send_verify"),
    # 校验验证码
    url(r'^check_verify/$', views.check_verify, name="check_verify"),
    # 登陆函数
    url(r'^login/$', views.Login.as_view(), name="login"),

    # 用户信息函数
    url(r'^info/$', is_login(views.UserInfo.as_view()), name="info"),
    url(r'^order/(\d+)/$', is_login(views.UserOrder.as_view()), name="order"),
    url(r'^site/$', is_login(views.UserSite.as_view()), name="site"),


    # 用户退出函数
    url(r'^exit/$', views.Exit.as_view(), name="exit"),

    # 用户忘记密码
    url(r'^f_pwd', views.ForgetPassword.as_view(), name='f_pwd'),

    # 图片验证码
    url(r"^code/$", views.code, name="code"),

    # 检测图片验证码是否正确
    url(r'^check_code/$', views.check_code, name="check_code"),

    url(r'^user_exist/$', views.user_exist, name="user_exist"),

    url(r'^check_id/$', views.check_id, name="check_id"),
    url(r'^get_alert_pwd/$', views.get_alert_pwd, name="get_alert_pwd"),
    url(r'^post_alert_pwd/$', views.post_alert_pwd, name="post_alert_pwd"),
    url(r'^alert_ok/$', views.alert_ok, name="alert_ok"),

]