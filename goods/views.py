from django.shortcuts import render

from . import models

from django.db.models import Q

from celery_tasks import tasks
from django.core.paginator import *
from users import models as um
from cart import models as cm
from order.models import OrderDetail

from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    '''首页处理函数'''
    r_c_imgs, s_imgs, all_cat = tasks.index_task()
    if request.session.has_key('loginUser'):
        name = request.session['loginUser']
        user = um.Users.objects.get(user_name=name)
        carts = cm.CartInfo.objects.filter(user=user)
        cart_count = 0
        for cart in carts:
            cart_count += cart.count
        return render(request, "goods/index.html", {"info": "首页",
                                                    "name": name,
                                                    "r_c_imgs": r_c_imgs,
                                                    "s_imgs": s_imgs,
                                                    "all_cat": all_cat,
                                                    "cart_count": cart_count
                                                    })
    else:
        return render(request, "goods/index.html", {"info": "首页",
                                                    "name": 0,
                                                    "r_c_imgs": r_c_imgs,
                                                    "s_imgs": s_imgs,
                                                    "all_cat": all_cat,
                                                    "cart_count": 0
                                                    })


def goods_list(request, tid, pindex, sort):
    '''

    :param request:
    :param cat: 商品类别的id
    :return:
    '''

    cat = models.Category.objects.get(id=int(tid))
    all_cat = models.Category.objects.all()
    # 新品上架
    news = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                           Q(goods_status="aa")).order_by('-goods_shelf_time')[0: 2]

    # 根据需求返回需要的数据
    if sort == "1":
        goods = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                               Q(goods_status="aa")).order_by('-goods_shelf_time')
    elif sort == "2":
        goods = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                               Q(goods_status="aa")).order_by('goods_price')
    elif sort == "3":
        goods = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                                Q(goods_status="aa")).order_by('-goods_click_rate')
    paginator = Paginator(goods, 10)

    try:
        page = paginator.page(int(pindex))
    except PageNotAnInteger:
        page = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面内容')
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if request.session.has_key('loginUser'):
        name = request.session['loginUser']

        context = {
            "name": name,
            "info": "列表页",
            "c_name": cat,
            "all_cat": all_cat,
            "news": news,
            "goods": goods,
            "sort": sort,
            'page': page,
            'paginator': paginator
        }
        return render(request, "goods/list.html", context)
    else:
        context = {
            "name": 0,
            "info": "列表页",
            "c_name": cat,
            "all_cat": all_cat,
            "news": news,
            "goods": goods,
            "sort": sort,
            'page': page,
            'paginator': paginator
        }
        return render(request, "goods/list.html", context)


def goods_detail(request, gid):
    '''

    :param request:
    :param gid: 商品编号
    :return:
    '''
    all_cat = models.Category.objects.all()
    good = models.GoodsInfo.objects.get(id=int(gid))
    good.goods_click_rate += 1
    good.save()
    good_detail = models.GoodsDetail.objects.get(goods=good)
    comments = OrderDetail.objects.filter(goods=good)
    news = models.GoodsInfo.objects.filter(Q(category=good.category) &
                                           Q(goods_status="aa")).order_by('-goods_shelf_time')[0: 2]
    if request.session.has_key('loginUser'):
        name = request.session['loginUser']
        # 有关最近浏览
        user = um.Users.objects.get(user_name=request.session['loginUser'])

        count = models.Recently.objects.filter(user_id=user.id).count()
        c = models.Recently.objects.filter(Q(user_id=user.id) & Q(goods_id=int(gid)))
        r_g = models.Recently()
        r_g.user_id = user.id
        r_g.goods_id = int(gid)
        if count <= 5:
            if c.count() == 0:
                r_g.save()
            else:
                c[0].delete()
                r_g.save()
        else:
            b = models.Recently.objects.filter(user_id=user.id).order_by('id')
            b[0].delete()
            if c.count() == 0:
                r_g.save()
            else:
                c[0].delete()
                r_g.save()

        context = {
            "name": name,
            "info": "商品详情",
            "good": good,
            "goods_detail": good_detail,
            "news": news,
            "all_cat": all_cat,
            "comments": comments
        }

        return render(request, "goods/detail.html", context)
    else:
        context = {
            "name": 0,
            "info": "商品详情",
            "good": good,
            "goods_detail": good_detail,
            "news": news,
            "all_cat": all_cat,
            "comments": comments
        }

        return render(request, "goods/detail.html", context)


def draw(request):
    return render(request, "draw/c_j.html")