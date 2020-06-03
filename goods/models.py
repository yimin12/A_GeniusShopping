from django.db import models

# Create your models here.
"""
商品种类模型
"""
class Category(models.Model):
    cname = models.CharField(max_length=30)
    def __str__(self):
        return u'Category:%s'%self.cname
"""
商品模型
"""
class Goods(models.Model):
    gname = models.CharField(max_length=100) # 商品名字
    gdesc = models.CharField(max_length=100) # 商品描述
    oldprice = models.DecimalField(max_digits=5,decimal_places=2) # 商品原价 e.g: 3.14
    price = models.DecimalField(max_digits=5,decimal_places=2) # 商品现价
    category = models.ForeignKey(Category,on_delete=models.CASCADE) # 商品种类连接外键
    def __str__(self):
        return u'Goods:%s'%self.gname
    def getGImg(self):
        # 通过Goods获得商品Color的信息， Goods -> Inventory -> Color,获取商品大图
        return self.inventory_set.first().color.colorurl
    # 获取商品所有的颜色对象
    def getColorList(self):
        colorList = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colorList:
                colorList.append(color)
        return colorList
    # 获取商品所有的Size对象
    def getSizeList(self):
        sizeList = []
        for inventory in self.inventory_set.all():
            size = inventory.size;
            if size not in sizeList:
                sizeList.append(size)
        return sizeList
    # 获取所有的详细信息
    def getDetailList(self):
        import collections
        # 创建一个有序字典用于存放详细信息(key:详情名称，value:图片列表)
        datas = collections.OrderedDict()
        for goodsdetail in self.goodsdetail_set.all():
            gdname = goodsdetail.name()
            if gdname not in datas:
                datas[gdname] = [goodsdetail.gdurl]
            else:
                datas[gdname].append(goodsdetail.gdurl)
        return datas
"""
商品细节名称模型
"""
class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)
    def __str__(self):
        return u'GoodsDetailName:%s'%self.gdname
"""
商品细节模型
"""
class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

    def name(self):
        return self.gdname.gdname
"""
商品根据大小分类模型
"""
class Size(models.Model):
    sname = models.CharField(max_length=10)
    def __str__(self):
        return u'Size:%s'%self.sname
"""
商品根据颜色分类模型
"""
class Color(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')
    def __str__(self):
        return u'Color:%s'%self.colorname
"""
库存 模型
"""
class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)