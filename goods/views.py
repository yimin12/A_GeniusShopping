import math

from django.shortcuts import render

# Create your views here.
from django.views import View
from goods.models import *
from django.core.paginator import Paginator
from django.http.response import HttpResponseBase

# 主页显示
class IndexView(View):
    def get(self, request, cid=1, num=1):
        # 所有通过url位置传参传入进来的都需要进行强转，以免抛出异常
        cid = int(cid)
        num = int(num)

        # step1: 查询所有类别信息
        categorys = Category.objects.all().order_by('id')
        # step2: 查询当前类别下的所有信息(给个默认值女装：id=2)
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')
        # step3: 分页，每页显示8条记录
        pager = Paginator(goodsList, 8)
        # step4: 获取当前页的数据
        page_goodList = pager.page(num)
        # step5: 处理首页和尾页(假设一共显示10页，选择页在list正中间)
        begin = (num - int(math.ceil(10.0 / 2)))
        # 首页禁止越界
        if begin < 1:
            begin = 1
        # 尾页禁止越界
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages
        if end <= 10:
            begin = 1
        else:
            begin = end - 9
        pagelist = range(begin, end + 1)
        return render(request, 'index.html',
                      {'categorys': categorys, 'goodList': page_goodList, 'currentCid': cid, 'pagelist': pagelist,
                       'currentNum': num})


# 使用二阶装饰器来构建缓存，实现“猜你喜欢”功能(保存你浏览过的网页的数据) 使用的是LCU
def recommend_view(func):
    def wrapper(detailView, request, goodsid, *args, **kwargs):
        # 将存放在cookie中的goodsId获取
        cookie_str = request.COOKIES.get('recommend', '')
        # 存放所有goodsid的列表
        goodsIdList = [gid for gid in cookie_str.split() if gid.strip()]

        # 思考1：最终需要获取的推荐商品
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsIdList if
                        gsid != goodsid and Goods.objects.get(id=gsid).category_id == Goods.objects.get(
                            id=goodsid).category_id][:4]
        # 将goodsObjList传递给get方法
        response = func(detailView, request, goodsid, goodsObjList, *args, **kwargs)
        # 判断goodsid是否存在goodsIdList中
        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0, goodsid)
        else:
            goodsIdList.insert(0, goodsid)
        # goodsIdList中的int转化成str
        goodsIdList = [str(x) for x in goodsIdList]
        # 将goodsIdList中的数据保存到Cookie中
        response.set_cookie('recommend', str(" ".join(goodsIdList)))
        return response
    return wrapper


class DetailView(View):
    @recommend_view
    def get(self, request, goodsid, recommendList=[]):
        goodsid = int(goodsid)
        # 根据goodsid查询商品详情信息（goods对象）
        goods = Goods.objects.get(id=goodsid)
        return render(request, 'detail.html', {'goods': goods, 'recommendList': recommendList})