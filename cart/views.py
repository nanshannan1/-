from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from . import models
from users import models as um
from goods import models as gm

from users.decorators import is_login


# Create your views here.
# 购物车界面函数
@is_login
def cart(request):
    name = request.session['loginUser']
    user = um.Users.objects.get(user_name=request.session['loginUser'])
    carts = models.CartInfo.objects.filter(user_id=user.id)
    count = carts.count()
    return render(request, "cart/cart.html", {'carts': carts, 'count': count, "name": name, "info": "购物车界面"})


# 添加购物车函数
@is_login
def add(request, gid, count):
    user = um.Users.objects.get(user_name=request.session['loginUser'])
    gid = int(gid)
    count = int(count)

    # 查询购物车中是否已经由此商品，如果有数量增加，如果没有则新增
    carts = models.CartInfo.objects.filter(user_id=user.id, goods_id=gid)
    if len(carts) >= 1:
        c = carts[0]
        c.count = c.count + count
        c.save()
    else:
        c = models.CartInfo()
        c.user_id = user.id
        c.goods_id = gid
        c.count = count
        c.save()

    if request.is_ajax():
        count = models.CartInfo.objects.filter(user_id=user.id).count()
        return JsonResponse({'count': count})
    else:
        return redirect("/cart/cart")


# 对购物车中的数据进行编辑，增加、减少
@is_login
def edit(request, cart_id, count):
    try:
        c = models.CartInfo.objects.get(pk=int(cart_id))
        count1 = c.count = int(count)
        c.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
        print(e)
    return JsonResponse(data)


# 删除购物车中的数据
@is_login
def delete(request, cart_id):
    try:
        c = models.CartInfo.objects.get(pk=int(cart_id))
        print(c)
        c.delete()
        data = {'ok': 1}
    except Exception as e:
        print(e)
        data = {'ok': 0}
    return JsonResponse(data)