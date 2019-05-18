from django.db import models


# Create your models here.
class Category(models.Model):
    '''
    商品类别表
    '''
    type_name = models.CharField(max_length=20, verbose_name="类别名称")
    type_logo = models.CharField(max_length=20, verbose_name="类别标志")
    type_image = models.ImageField(upload_to="type/", verbose_name="类别图片")

    class Meta:
        db_table = "category"
        verbose_name = "商品类别表"
        verbose_name_plural = "商品类别"

    def __str__(self):
        return self.type_name


class GoodsInfo(models.Model):
    '''
    商品信息表
    '''
    UNIT = (("a", u"kg/元"), ("b", u"斤/元"), ('c', u'个/元'))
    STATUS = (("aa", u"上架"), ("bb", u"下架"))
    goods_name = models.CharField(max_length=25, verbose_name="商品名称")
    goods_img = models.ImageField(upload_to="goods/", verbose_name="商品图片")
    goods_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="商品价格")
    goods_unit = models.CharField(max_length=10, verbose_name="单位", choices=UNIT)
    goods_repertory = models.IntegerField(verbose_name="库存")  # 库存
    goods_status = models.CharField(max_length=10, choices=STATUS,
                                    verbose_name="状态")  # 0 上架 1 下架
    goods_click_rate = models.IntegerField(verbose_name="点击量", default=0)  # 点击量
    goods_shelf_time = models.DateTimeField(verbose_name="上架时间")  # 上架时间
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="商品类别")

    class Meta:
        db_table = "goodsinfo"
        verbose_name = "商品信息表"
        verbose_name_plural = "商品信息"

    def __str__(self):
        return self.goods_name


class GoodsDetail(models.Model):
    '''
    商品详情表
    '''
    desc = models.TextField(verbose_name="商品描述")
    desc_detail = models.TextField(verbose_name="商品详情")
    goods = models.OneToOneField(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品")

    class Meta:
        db_table = "goodsdetail"
        verbose_name = "商品描述表"
        verbose_name_plural = "商品描述"


class RotationChart(models.Model):
    '''
    首页轮播图表
    '''
    r_c_img = models.ImageField(upload_to="rotationchart/", verbose_name="首页轮播图")

    class Meta:
        db_table = "rotationchart"
        verbose_name = "首页轮播图表"
        verbose_name_plural = "首页轮播图"


class Sales(models.Model):
    '''
    图片表
    '''
    s_img = models.ImageField(upload_to="sales/", verbose_name="热销商品")

    class Meta:
        db_table = "Sales"
        verbose_name = "热销图片表"
        verbose_name_plural = "热销图片"


class Recently(models.Model):
    '''
    最近浏览的商品表
    '''
    user = models.ForeignKey("users.Users")
    goods = models.ForeignKey("goods.GoodsInfo")

    class Meta:
        db_table = "recently"

