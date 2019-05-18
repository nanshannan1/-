# -*- coding: utf-8 -*-
import random


import hashlib


def code():
    '''发送验证码'''
    s = ''  # 创建字符串变量，存储生成的验证码
    for i in range(6):
        num = random.randint(0, 9)
        s = s + str(num)
    return s


# 密码加密
def hashlib_sha512(pwd):
    result = hashlib.sha512(pwd).hexdigest()
    return result




