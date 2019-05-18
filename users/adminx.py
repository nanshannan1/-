import xadmin
from . import models
from xadmin import views


class BaseSetting(object):
    '''可以设置主题,作用与全局'''
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    '''修改样式,作用与全局'''
    site_title = "生鲜超市后台管理系统"
    site_footer = "CopyRight © 2019 西华生鲜超市责任有限公司 All Rights Reserved"
    # 左侧菜单可以折叠
    # menu_style = "accordion"


class UsersAdmin(object):
    list_display = ['user_name', 'user_phone', 'user_email',
                    'register_time', 'last_login_time']
    search_fields = ['user_name', 'user_email']
    list_filter = ['user_name', 'user_email', 'register_time']
    # 设置只读字段
    # readonly_fields = ['id']
    refresh_times = [5, 7]

    # 不允许删除、添加、修改
    remove_permissions = ('delete', 'add', 'change')
    # 分页每次显示10条
    list_per_page = 10


class AddressAdmin(object):
    list_display = ['addressee', 'direction',
                    'zip_code', 'addressee_contact', 'user']

    # 不允许删除、添加、修改
    remove_permissions = ('delete', 'add', 'change')
    # 分页每次显示10条
    list_per_page = 10


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(models.Users, UsersAdmin)
xadmin.site.register(models.Address, AddressAdmin)