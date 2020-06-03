from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import *


class AddCartView(View):
    def post(self,request):
        # 在多级字典数据的时候，需要手动设置modified=True，实时的将modified数据存如session对象中
        # 在多级字典中，可能并不会实时更新
        request.session.modified = True
        # step 1: 获取当前操作类型
        flag = request.POST.get('flag','')
        # step 2: 判断当前操作类型
        # 同步操作信息到数据库中
        if flag == 'add':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 加如购物车操作
            carManagerObj.add(**request.POST.dict())
        if flag == 'plus':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            carManagerObj.update(step=1,**request.POST.dict())
        if flag == 'minus':
            carManagerObj = getCartManger(request)
            carManagerObj.update(step=-1,**request.POST.dict())
        if flag == 'delete':
            carManagerObj = getCartManger(request)
            carManagerObj.delete(**request.POST.dict())
        return HttpResponseRedirect('/cart/queryAll/')

class CartListView(View):
    def get(self,request):
        # 创建cartManager对象
        carManagerObj = getCartManger(request)
        # 查询所有购物项的信息
        cartList = carManagerObj.queryAll()
        return render(request,'cart.html',{'cartList':cartList})