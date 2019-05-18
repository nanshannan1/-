from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

from users.models import Users
from users.models import Address
from goods.models import GoodsInfo
from cart.models import CartInfo
from . import models
from sxcs.settings import BASE_DIR
from users.decorators import is_login

from alipay import AliPay

import os
import time


# Create your views here.
@is_login
@transaction.atomic
def single_order(request, g_id, count):
    name = request.session['loginUser']

    user = Users.objects.get(user_name=name)
    address = Address.objects.filter(user=user).order_by('-id')
    good = GoodsInfo.objects.select_for_update().get(pk=int(g_id))

    total_price1 = good.goods_price * int(count)

    total_price2 = good.goods_price * int(count) + 10

    t_s = transaction.savepoint()
    order = models.Order(user=user,
                         order_address=address[0],
                         total_price=total_price2,
                         total_count=int(count),
                         )
    order.save()

    if int(count) < good.goods_repertory:
        order_detail = models.OrderDetail(goods=good,
                                          order=order,
                                          price=total_price1,
                                          count=int(count))

        order_detail.save()
        transaction.savepoint_commit(t_s)
    else:
        transaction.savepoint_rollback(t_s)
        return JsonResponse({"msg": "商品库存不足"})

    context = {
        "address": address,
        "good": good,
        "total_price1": total_price1,
        "total_price2": total_price2,
        "count": count,
        "info": "提交订单",
        "name": name,
        "order_id": order.id
    }
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(order.id)
    return render(request, "order/place_order.html", context)


@is_login
@transaction.atomic
def many_goods(request):
    name = request.session['loginUser']
    user = Users.objects.get(user_name=name)
    address = Address.objects.filter(user=user).order_by("-id")
    cart_id = request.GET.get("checkID")
    cart_id = cart_id.split(',')

    # 所有的购物车记录
    all_cart = []

    # 购买商品所需的费用
    total_price1 = 0
    # 购买商品加邮费的费用
    total_price2 = total_price1 + 10
    # 总共购买了几件商品
    total_num = 0
    # 显示的序号
    num = 1

    # 设置保存点
    s_t = transaction.savepoint()

    order = models.Order(user=user,
                         order_address=address[0],
                         total_price=0,
                         total_count=0,
                         )
    order.save()

    for c in cart_id:

        cart = CartInfo.objects.get(pk=int(c))
        cart.cart_price = cart.count * cart.goods.goods_price

        cart.num = num
        num += 1

        all_cart.append(cart)

        total_price1 += cart.cart_price

        total_num += cart.count

        goods = cart.goods

        if cart.count > goods.goods_repertory:
            transaction.savepoint_rollback(s_t)
            return JsonResponse({"msg": "库存不足"})

        order_detail = models.OrderDetail(goods=goods,
                                          order=order,
                                          price=cart.cart_price,
                                          count=cart.count)
        order_detail.save()

        # 删除购物车中的记录
        cart.delete()

        # 修改库存
        goods.goods_repertory -= cart.count

    transaction.savepoint_commit(s_t)

    # 修改order表
    order.total_price = total_price2
    order.total_count = total_num
    order.save()

    context = {
        "name": name,
        "info": "提交订单",
        "address": address,
        "all_cart": all_cart,
        "total_price1": total_price1,
        "total_price2": total_price2,
        "total_num": total_num,
        "order_id": order.id

    }

    return render(request, "order/place_order2.html", context)


def payment(request):
    post = request.POST
    address_id = post.get("address_id")
    pay_style = post.get("pay_style")
    order_id = post.get("order_id")

    if request.session.has_key('loginUser'):
        user_name = request.session['loginUser']
        user = Users.objects.get(user_name=user_name)
        try:
            address = Address.objects.get(pk=address_id)

            order = models.Order.objects.get(Q(pk=order_id) & Q(user=user))
            order.order_address = address

            if pay_style == "3":
                order.pay_method = int(pay_style)
                order.save()

                app_private_key_string = open(BASE_DIR + '\\order\\private_key.pem').read()
                alipay_public_key_string = open(BASE_DIR + '\\order\\public_key.pem').read()

                alipay = AliPay(
                    appid="2016092800613199",
                    app_notify_url=None,
                    app_private_key_string=app_private_key_string,
                    alipay_public_key_string=alipay_public_key_string,
                    sign_type="RSA2",
                    debug=True

                )
                # print("11111111111111111133333333333333")
                # 调用支付接口
                order_string = alipay.api_alipay_trade_page_pay(
                    out_trade_no=order.id,
                    # Decimal类型需要转化成字符串
                    # total_amount=str(total_price),
                    total_amount="0.01",
                    subject="生鲜超市%s" %order.id,
                    return_url=None,
                    notify_url=None  # 可选, 不填则使用默认notify url
                )
                pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
                return JsonResponse({"code": 3, "pay_url": pay_url})

            else:
                # 2 暂不支持的支付类型
                return JsonResponse({"code": 2})

        except:
            # 0 订单错误
            return JsonResponse({"code": 0})
    else:
        # 1 用户未登录
        return JsonResponse({"code": 1})


def go_payment(request):
    print("q111111111111111111111111111111")
    order_id = request.POST.get("order_id")
    if request.session.has_key('loginUser'):
        user_name = request.session['loginUser']
        user = Users.objects.get(user_name=user_name)
        # order_id = request.POST.get("order_id")
        try:
            order = models.Order.objects.get(Q(pk=order_id) & Q(user=user))
            print("q111111111111111111111111111111")
            app_private_key_string = open(BASE_DIR + '\\order\\private_key.pem').read()
            alipay_public_key_string = open(BASE_DIR + '\\order\\public_key.pem').read()

            alipay = AliPay(
                appid="2016092800613199",
                app_notify_url=None,
                app_private_key_string=app_private_key_string,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",
                debug=True

            )
            print("22222222222222222222222222333333333333")
            # 调用支付接口
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order.id,
                # Decimal类型需要转化成字符串
                # total_amount=str(total_price),
                total_amount="0.01",
                subject="生鲜超市%s" %order.id,
                return_url=None,
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
            return JsonResponse({"code": 3, "pay_url": pay_url})



        except:
            # 0 订单错误
            return JsonResponse({"code": 0})

    else:
        return JsonResponse({"code": 1, "msg": "用户未登录"})


def pay_check(request):
    """
    查看订单支付结果
    :param request:
    :return:
    """
    order_id = request.POST.get("order_id")
    if request.session.has_key('loginUser'):
        user_name = request.session['loginUser']
        user = Users.objects.get(user_name=user_name)
        try:
            order = models.Order.objects.get(Q(pk=order_id) & Q(user=user))

            app_private_key_string = open(BASE_DIR + '\\order\\private_key.pem').read()
            alipay_public_key_string = open(BASE_DIR + '\\order\\public_key.pem').read()

            alipay = AliPay(
                appid="2016092800613199",
                app_notify_url=None,
                app_private_key_string=app_private_key_string,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",
                debug=True
            )
            while True:
                response = alipay.api_alipay_trade_query(order_id)
                code = response.get('code')
                if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                    # 支付成功
                    # 获取支付宝交易号
                    # 修改订单
                    order.order_status = 4
                    order.trade_no = response.get('trade_no')
                    order.save()
                    return JsonResponse({"info": 3, "msg": "支付成功"})

                elif code == '40004' or (code == '10000' and response['trade_status'] == 'WAIT_BUYER_PAY'):
                    # 等待支付
                    time.sleep(5)
                    continue

                else:
                    return JsonResponse({"info": 2, "msg": "支付失败"})
        except:
            return JsonResponse({"info": 1, "msg": "订单错误"})

    else:
        return JsonResponse({"info": 0, "msg": "用户未登录"})


def order_comment(request, o_d_i):
    if request.method == "GET":
        order_detail = models.OrderDetail.objects.get(id=int(o_d_i))
        return render(request, "order/comment.html", {"order": order_detail})
    elif request.method == "POST":
        comment = request.POST.get("comment")
        name = request.session['loginUser']
        user = Users.objects.get(user_name=name)
        print(comment)
        order_detail = models.OrderDetail.objects.get(id=int(o_d_i))
        if order_detail is not None:
            order_detail.comment = comment
            order_detail.comment_status = 1
            order_detail.save()
            return redirect(reverse('users:order', args=(user.id, )))
