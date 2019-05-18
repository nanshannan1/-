import xadmin
from . import models


class CategoryAdmin(object):
    list_display = ['type_name', 'type_logo', 'type_image']
    search_fields = ['type_name']
    list_filter = ['type_name']
    list_editable = ['type_name', 'type_logo', 'type_image']
    refresh_times = [5, 7]


class GoodsInfoAdmin(object):
    list_display = ['goods_name', 'goods_img', 'goods_price',
                    'goods_unit', 'goods_repertory', 'goods_status',
                    'goods_click_rate', 'goods_shelf_time', 'category']
    search_fields = ['goods_name', 'goods_price', 'goods_unit', 'goods_repertory',
                     'goods_status', 'goods_click_rate', 'goods_shelf_time', 'category']
    list_filter = ['goods_name', 'goods_price', 'goods_unit', 'goods_repertory',
                   'goods_status', 'goods_click_rate', 'goods_shelf_time', 'category']
    list_editable = ['goods_name', 'goods_img', 'goods_price',
                     'goods_unit', 'goods_repertory', 'goods_status',
                     'goods_shelf_time', 'category']
    # 显示可以让别人编辑的字段
    fields = ['goods_name', 'goods_img', 'goods_price',
              'goods_unit', 'goods_repertory', 'goods_status',
              'goods_shelf_time', 'category']
    refresh_times = [5, 7]


class GoodsDetailAdmin(object):
    list_display = ['desc', 'desc_detail', 'goods']
    search_fields = ['goods']
    list_editable = ['desc', 'desc_detail', 'goods']
    refresh_times = [5, 7]


class RotationChartAdmin(object):
    list_display = ['id', 'r_c_img']
    # 暂时允许添加，后期只允许修改
    # remove_permissions = ('delete', 'add')


class SalesAdmin(object):
    list_display = ['id', 's_img']
    # 暂时允许添加，后期只允许修改
    # remove_permissions = ('delete', 'add')


xadmin.site.register(models.Category, CategoryAdmin)
xadmin.site.register(models.GoodsInfo, GoodsInfoAdmin)
xadmin.site.register(models.GoodsDetail, GoodsDetailAdmin)
xadmin.site.register(models.RotationChart, RotationChartAdmin)
xadmin.site.register(models.Sales, SalesAdmin)
