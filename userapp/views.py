from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views import View

from cart.cartmanager import SessionCartManager
from userapp.models import *
from utils.code import gene_code


class RigisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        # 获取请求参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        # 插入数据库
        user = UserInfo.objects.create(uname=uname,pwd=pwd)
        # 假设user是存在的,我们使用重定向（非跳转）
        if user:
            # 然后将用户信息放置在session中(session放置在Cache中，(Cache建立在本机redis中)))老千层饼
            # 由于后期需要添加类似购物车这类型的feature，我们要使用全局上下文，则要建立mycontextprocessors
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')
        return HttpResponse('/user/register')

# 检查数据库中是否存在该用户
class CheckUnameView(View):
    def get(self,request):
        # 获取请求参数
        uname = request.GET.get('uname','')
        # 根据用户名去数据库中查询
        userList = UserInfo.objects.filter(uname=uname)
        flag = False
        if userList:
            flag = True
        return JsonResponse({'flag':flag})

class CenterView(View):
    def get(self,request):
        # 获取请求参数
        red = request.GET.get('redirect','')
        return render(request,'center.html',{'redirect':red})

class LogoutView(View):
    # 收到来自页面的ajax请求
    def post(self,request):
        # 删除session中用户登录的信息
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'delflag':True}) # 转化成json格式传给ajax

# 处理登陆信息
class LoginView(View):
    def get(self,request):
        # 获取请求参数
        red = request.GET.get('redirect','')
        if red:
            return render(request,'login.html',{'redirect':red})
        return render(request,'login.html')
    def post(self,request):
        # step1. 获取请求参数
        red = request.POST.get('redirect', '')
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        # step2. 根据获取的数据进入数据库查找数据
        userList = UserInfo.objects.filter(uname = uname,pwd = pwd)
        # step3. 如果userList有返回值
        if userList:
            request.session['user'] = userList[0]
            red = request.POST.get('redirect','')
            if red == 'cart':
                # 将session重点额购物项移动到数据库中
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/queryAll/')
            elif red == 'order':
                return HttpResponseRedirect('/order/order.html?cartitems=' + request.POST.get('cartitems',''))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login')

class LoadCodeView(View):
    def get(self,request):
        img, str = gene_code()
        # 将生成的代码放置在session中
        request.session['sessionCode'] = str
        return HttpResponse(img,content_type='image/png')

class CheckCodeView(View):
    def get(self,request):
        #获取输入框中的验证码
        code = request.GET.get('code','')
        #获取生成的验证码
        sessionCode = request.session.get('sessionCode',None)
        #比较是否相等
        flag = code == sessionCode
        return JsonResponse({'checkFlag':flag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        # 获取当前登录用户的所有收货地址(如果user是空值，user.address_set.all()，会报异常)
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})
    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')
        # 将数据插入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                                         isdefault=(lambda count: True if count == 0 else False)(
                                             user.address_set.all().count()))
        # 获取当前登录用户的所有收货地址
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

class LoadAreaView(View):
    def get(self,request):
        # 获取请求参数
        pid = request.GET.get('pid',-1)
        pid = int(pid)
        # 根据父id查询区划信息
        areaList = Area.objects.filter(parentid=pid)
        # 进行序列化
        jareaList = serialize('json',areaList)
        return JsonResponse({'jareaList':jareaList})