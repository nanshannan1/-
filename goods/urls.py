from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^index/$", views.index, name="index"),
    url(r"^goods_list/(\d+)/(\d+)/(\d+)/$", views.goods_list, name="goods_list"),
    url(r"^(\d+)/$", views.goods_detail, name="goods_detail"),
    url(r"^c_j/$", views.draw, name="c_j")

]