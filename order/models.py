from django.db import models


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey("users.Users", verbose_name="用户")
    order_address = models. ForeignKey("users.Address", verbose_name="收货地址")
    pay_method = models.IntegerField(default=3, verbose_name="支付方式")  # 1 货到付款 2 微信支付 3 支付宝 4 银联支付
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总计")
    total_count = models.IntegerField(default=1, verbose_name="商品的总数量")
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品运费", default=10.00)
    order_status = models.IntegerField(default=1, verbose_name="支付方式")  # 1 待支付 2 代发货 3 待评价 4 已完成
    order_date = models.DateTimeField(auto_now=True, verbose_name="购买时间")
    trade_no = models.CharField(max_length=128, default='', verbose_name='支付编号')

    class Meta:
        db_table = "order"
        verbose_name = "订单表"
        verbose_name_plural = "订单"

    def __str__(self):
        return self.trade_no


class OrderDetail(models.Model):
    goods = models.ForeignKey("goods.GoodsInfo", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    comment = models.TextField(verbose_name="商品评论", default="")
    comment_status = models.IntegerField(verbose_name='是否评论', default=0)  # 0 未评论 1 评论完成

    class Meta:
        db_table = "orderdetail"
        verbose_name = "订单详情表"
        verbose_name_plural = "订单详情"

    # def __str__(self):
    #     return self.count



