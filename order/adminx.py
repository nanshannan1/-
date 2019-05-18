import xadmin
from . import models


# Register your models here.
class OrderAdmin(object):
    list_display = ["user", "order_address", "pay_method",
                    "total_price",
                    "order_date", "trade_no"]
    # search_fields = ["user"]
    list_filter = ["user"]
    # 不允许删除、添加、修改
    remove_permissions = ('delete', 'add', 'change')
    # 分页每次显示10条
    list_per_page = 10

    def queryset(self):
        qs = super(OrderAdmin, self).queryset()
        return qs.filter(order_status=4)


class OrderDetailAdmin(object):
    list_display = [
        "goods", "order",
        "price", "count"
    ]

    # 不允许删除、添加、修改
    remove_permissions = ('delete', 'add', 'change')
    # 分页每次显示10条
    list_per_page = 10

    def queryset(self):
        qs = super(OrderDetailAdmin, self).queryset()
        return qs.filter(order_id__order_status=4)


xadmin.site.register(models.Order, OrderAdmin)
xadmin.site.register(models.OrderDetail, OrderDetailAdmin)
