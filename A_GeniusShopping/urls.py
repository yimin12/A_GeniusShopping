"""A_GeniusShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from A_GeniusShopping.settings import DEBUG, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('goods.urls')),
    path('user/', include('userapp.urls')),
    path('cart/', include('cart.urls')),
    path('order/',include('order.urls')),
]

# 在开发模式下，处理文件上传的操作
if DEBUG:
    from django.views.static import serve
    urlpatterns.append(re_path('media/(.*)',serve,kwargs={'document_root':MEDIA_ROOT}))