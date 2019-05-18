from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^single_order/(\d+)/(\d+)/$", views.single_order, name="single_order"),
    url(r"^many_goods/$", views.many_goods, name="many_goods"),
    url(r"^payment/$", views.payment, name="payment"),
    url(r"^go_payment/$", views.go_payment, name="go_payment"),
    url(r"^pay_check/$", views.pay_check, name="pay_check"),
    # 订单评价
    url(r"^comment/(\d+)$", views.order_comment, name="comment"),
]