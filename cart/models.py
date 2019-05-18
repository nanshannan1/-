from django.db import models


# 商品购物车模块
# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey("users.Users")
    goods = models.ForeignKey("goods.GoodsInfo")
    count = models.IntegerField()

    class Meta:
        db_table = "cart"
