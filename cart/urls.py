from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^cart/$', views.cart, name="cart"),
    url(r'^add(\d+)_(\d+)/$', views.add, name="add"),
    url(r'^edit(\d+)_(\d+)/$', views.edit, name="edit"),
    url(r'^delete(\d+)/$', views.delete, name="delete"),
]