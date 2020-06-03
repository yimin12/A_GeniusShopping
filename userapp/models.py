# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# 由数据库表逆向生成了地区模型
class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False   # 标识在正向生成的时候不会再创建这个表
        db_table = 'area'

# 处理用户登陆信息，以及地址管理系统
# 登陆用户信息模型
class UserInfo(models.Model):
    uname = models.EmailField(max_length=100)
    pwd = models.CharField(max_length=100)
    def __str__(self):
        return u'UserInfo:%s'%self.uname

# 地址模型
class Address(models.Model):
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    isdefault = models.BooleanField(default=False) # 是否默认地址
    userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    def __str__(self):
        return u'Address:%s'%self.aname