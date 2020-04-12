from django.db import models


# Create your models here.
from App.views_constant import ORDER_STATUS_NOT_PAY


class MainWheel(models.Model):
    # axf_wheel(img,name,trackid)

    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_wheel'


class FoodType(models.Model):
   typeid = models.IntegerField(default=1)
   typenames = models.CharField(max_length=12)
   childtypenames = models.CharField(max_length=255)
   typesort = models.IntegerField(default=1)
   class Meta:
       db_table = 'axf_foodtype'



class Goods(models.Model):
    productid = models.CharField(
        max_length=20
    )
    productimg = models.CharField(
        max_length=255
    )
    productname = models.CharField(
        max_length=100
    )
    productlongname = models.CharField(
        max_length=200
    )
    isxf = models.BooleanField(
        default=0
    )
    pmdesc = models.BooleanField(
        default=0
    )
    specifics = models.CharField(
        max_length=40
    )
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(
        max_length=100
    )
    dealerid = models.CharField(
        max_length=30
    )
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        db_table = "axf_goods"


class AXFUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icons/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'


class Cart(models.Model):
    c_user = models.ForeignKey(AXFUser,on_delete=None)
    c_goods = models.ForeignKey(Goods,on_delete=None)

    c_goods_nums = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)
    class Meta:
        db_table = 'axf_cart'


class Order(models.Model):
    o_user = models.ForeignKey(AXFUser,on_delete=None)
    o_price = models.FloatField()
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)
    o_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'axf_oder'


class OrderGoods(models.Model):
    og_goods = models.ForeignKey(Goods,on_delete=None)
    og_goods_num = models.IntegerField(default=1)
    og_order = models.ForeignKey(Order,on_delete=None)
    class Meta:
        db_table = 'axf_ordergoods'
