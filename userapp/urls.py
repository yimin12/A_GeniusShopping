#encoding=utf-8
from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RigisterView.as_view()),
    path('checkUname/',views.CheckUnameView.as_view()), # 专门验证用户密码
    path('center/',views.CenterView.as_view()), # 进入登录之后的页面
    path('logout/',views.LogoutView.as_view()), # 处理对出登录
    path('login/',views.LoginView.as_view()), # 专门处理登录页面
    path('loadCode.jpg', views.LoadCodeView.as_view()), # 处理验证码刷新
    path('checkcode/', views.CheckCodeView.as_view()), # 校验验证码
    path('address/',views.AddressView.as_view()), # 处理收货地址
    path('loadArea/',views.LoadAreaView.as_view()) # 加載數據庫中的地址信息
]