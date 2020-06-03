#coding=utf-8
from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns=[
    path('',views.IndexView.as_view()),
    path('category/<int:cid>',views.IndexView.as_view()),
    path('category/<int:cid>/page/<int:num>/',views.IndexView.as_view()),
    # re_path(r'^category/(?P<cid>[0-9]{1})/page/(?P<num>[0-9]{1})/$',views.IndexView.as_view()),
    path('goodsdetails/<int:goodsid>',views.DetailView.as_view())
]
# 不知为何使用位置传参一直有错
