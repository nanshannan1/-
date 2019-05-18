from django.db import models


# Create your models here.
class Users(models.Model):
    user_name = models.CharField(max_length=10, verbose_name="用户名")
    user_pwd = models.CharField(max_length=200, verbose_name="密码")
    user_phone = models.CharField(max_length=11, null=True, verbose_name="手机号")
    user_email = models.CharField(max_length=40, verbose_name="邮箱")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_login_time = models.DateTimeField(auto_now=True, verbose_name="最近登录时间")

    class Meta:
        db_table = "users"
        verbose_name = "用户表"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.user_name


class Address(models.Model):
    addressee = models.CharField(max_length=10, null=True, verbose_name="收件人")
    direction = models.TextField(null=True, verbose_name="收货地址")
    zip_code = models.CharField(max_length=6, null=True, verbose_name="邮政编号")
    addressee_contact = models.CharField(max_length=11, null=True, verbose_name="联系方式")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="寄件人")

    class Meta:
        db_table = "address"
        verbose_name = "地址表"
        verbose_name_plural = "地址"

    def __str__(self):
        return self.addressee



