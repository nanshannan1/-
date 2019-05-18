from celery import Celery
from goods import models
from django.db.models import Q
from django.core.cache import cache

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker="redis://127.0.0.1:6379/2")


# 定义任务函数
def index_task():
    '''
    首页静态页面任务函数
    '''
    r_c_imgs = cache.get("r_c_imgs")
    s_imgs = cache.get("s_imgs")
    all_cat = cache.get("all_cat")

    if r_c_imgs is None and s_imgs is None and all_cat is None:
        # 获取首页轮播图
        r_c_imgs = models.RotationChart.objects.all().order_by("-id")[0: 3]
        cache.set("r_c_imgs", r_c_imgs)
        # 获取促销总览图片
        s_imgs = models.Sales.objects.all().order_by("-id")[0: 2]
        cache.set("s_imgs", s_imgs)
        # 查询商品的种类信息
        category = models.Category.objects.all()

        all_cat = []
        i = 0
        for cat in category:
            new_goods = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                                        Q(goods_status="aa")).order_by('-goods_shelf_time')[0: 4]
            hot_goods = models.GoodsInfo.objects.filter(Q(category=cat.id) &
                                                        Q(goods_status="aa")).order_by('-goods_click_rate')[0: 4]
            print(hot_goods)
            i += 1

            cat.mid = i
            cat.new_goods = new_goods
            cat.hot_goods = hot_goods

            all_cat.append(cat)
        cache.set("all_cat", all_cat)

    return r_c_imgs, s_imgs, all_cat

