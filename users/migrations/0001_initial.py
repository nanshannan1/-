# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-20 01:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressee', models.CharField(max_length=10, null=True, verbose_name='收件人')),
                ('direction', models.TextField(null=True, verbose_name='收货地址')),
                ('zip_code', models.CharField(max_length=6, null=True, verbose_name='邮政编号')),
                ('addressee_contact', models.CharField(max_length=11, null=True, verbose_name='联系方式')),
            ],
            options={
                'verbose_name': '地址表',
                'verbose_name_plural': '地址',
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=10, verbose_name='用户名')),
                ('user_pwd', models.CharField(max_length=200, verbose_name='密码')),
                ('user_phone', models.CharField(max_length=11, null=True, verbose_name='手机号')),
                ('user_email', models.CharField(max_length=40, verbose_name='邮箱')),
                ('register_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('last_login_time', models.DateTimeField(auto_now=True, verbose_name='最近登录时间')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户',
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users', verbose_name='寄件人'),
        ),
    ]