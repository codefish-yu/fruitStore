from django.contrib import admin
from .models import *
# Register your models here.




class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title','goodsType','price','spec','isActive')
    #加上过滤器
    list_filter = ('goodsType','isActive')
    search_fields = ('title',)
    list_editable = ('price','spec')

#将模型管理器类和模型类进行绑定
admin.site.register(Goods,GoodsAdmin)
admin.site.register(GoodsType)