from django.db import models

# Create your models here.

class User(models.Model):
    upthone = models.CharField(max_length=11,verbose_name='手机号')
    upwd = models.CharField(max_length=32,verbose_name='密码')
    uname = models.CharField(max_length=20,verbose_name='用户名')
    uemail = models.EmailField(verbose_name='邮箱')
    isActive = models.BooleanField(default=True,verbose_name='是否激活')


    class Meta:
        db_table = 'User'

    def __str__(self):
        return '< %s %s %s %s %s>'%(self.upthone,self.upwd,self.uname,self.uemail,self.isActive)


class GoodsType(models.Model):

    title = models.CharField(max_length=20,verbose_name='品类名')
    desc = models.CharField(max_length=200,verbose_name='品类描述')

    class Meta:
        db_table = 'goods_type'
        verbose_name = '商品类别'
        #将单数显示形式赋值给复数,才能显示单数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Goods(models.Model):
    title = models.CharField(max_length=40,verbose_name="商品名称")
    price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name="价格")
    spec = models.CharField(max_length=20,verbose_name='规格')
    picture = models.ImageField(upload_to='static/upload/goods',verbose_name='商品图片')
    # 外键
    goodsType = models.ForeignKey(GoodsType)
    isActive = models.BooleanField(default=True,verbose_name='是否上架')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goods'
        verbose_name= '商品'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title



