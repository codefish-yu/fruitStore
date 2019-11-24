# from django.shortcuts import render
#
# # Create your views here.
# def index(request):
#         return render(request,'index.html')

import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.

#单独一个试图，拿index
def index(request):
    return render(request,'index.html')


#拿完index,点首页点注册,进入注册功能，得先配置首页ajax
def register(request):
    # 注册成功后# 免登陆1天session
    # ##以下为不用ajax的写法,验证的逻辑和不同页面的获取写在同一个试图函数中
    #拿注册页面
    if request.method == 'GET':
        return render(request, 'register.html')
    # 处理注册数据
    elif request.method == 'POST':
        #从请求体中取出数据,不是前后端分离，直接用request.post方法
        telephone = request.POST.get('telephone')

        old_user = User.objects.filter(upthone=telephone)
        if old_user:
            dic = {'msg': '当前用户已存在'}
            return render(request,'register.html',dic)

        password = request.POST.get('password')
        username = request.POST.get('username')
        email = request.POST.get('email')
        #TODO 验证用户名是否存在，验证数据是否为空

        #创建用户，upthon等为数据表中的字段名
        user = User.objects.create(upthone=telephone,upwd=password,uname=username,uemail=email)
        #记录登录状态，存session,在哪里设置session的保存时间？
        request.session['username'] = username
        request.session['uid'] = user.id

        # 重定向到首页
        return  HttpResponseRedirect('/index/')

# 登录功能
def login(request):
    if request.method == 'GET':
        # GET请求cookies和session流程：先检查是否有session,若有session直接去首页，
        # 若无session,检查cookies,若有cookies,回写session
        # ,若无cookies,则让他去登录
        # 1,检查session
        if 'username' in request.session:
            # 有session，已经登录
            return HttpResponseRedirect('/index/')
        # 2,检查cookies
        if 'username' in request.COOKIES:
            # cookies有数据(已登录)&session没数据，回写session
            request.session['username'] = request.COOKIES['username']
            return HttpResponseRedirect('/index/')

        return render(request,'login.html')
    elif request.method == 'POST':

        # #客户端从form中提交post请求,数据在请求体中传递给后端，后端用这个拿
        username = request.POST.get('username')
        password = request.POST.get('userpass')

        # 登录
        users = User.objects.filter(uname=username)  # 取出的是对象的queryset(列表形式)
        if users:
            if users[0].upwd == password:
                # 记录登录状态
                # POST请求cookies和session流程：先存session,
                # 按客户需存cookies，若满足帐号密码跳转到首页

                # 保存session值到数据库
                request.session['username'] = username
                request.session['uid'] = users[0].id
                # 检查永不是否点了记住密码
                resp = HttpResponseRedirect('/index/')
                save_cookies = False
                # checkbox复选框的数据也在request.POST中
                # 如果能够从请求体中取出checkbox的数据(请求体是类字典)，就说明用户点了记住密码
                if 'save_cookies' in request.POST.keys():
                    save_cookies = True
                if save_cookies:
                    # cookies中存储用户状态
                    # 语法：resp.set_cookie('cookies名',cookies值,超时时间)
                    resp.set_cookie('username', username, 60 * 60 * 24 * 30)
                    resp.set_cookie('uid', users[0].id, 60 * 60 * 24 * 30)

                return resp

#退出功能
#需求：清cookies,清session,重定向到首页
def logout(request):
    if 'username' in request.session and 'uid' in request.session:
        #删除session
        del request.session['username']
        del request.session['uid']
    resp = HttpResponseRedirect('/index/')

    if 'username' in request.COOKIES and 'uid' in request.COOKIES:
        resp.delete_cookie('username')
        resp.delete_cookie('uid')

    return resp

# 用于ajax向后端发来请求时的判断响应，是否已登录
def check_session(request):
    # 获取session: request.session['key']
    # 如果有session说明登录着呢
    session_value = request.session.get('username')  # session是字典形式
    if session_value:
        # 登录的返回
        # 用json串序列化返回
        res = {'loginStage': 1, 'username': session_value}
        return JsonResponse(res)

    # 如果没有session,去检查cookies,如果有cookies则回写session,\
    # 如果没有则显示登录
    cookies_value = request.COOKIES.get('username')  # cookies也是字典形式存储
    if cookies_value:
        # cookies有数据(已登录)&session没数据，回写session
        request.session['username'] = request.COOKIES['username']
        res = {'loginStage': 1, 'username': cookies_value}
        return JsonResponse(res)
    else:
        # 未登录的返回
        res = {'loginStage': 0}
        return JsonResponse(res)

def load_goods(request):
    # 加载商品
    # [{'type':{'title':'热带水果'},'goods':[{},{},...]},...]
    # type的数据在表:goodstype中取,goods的数据在表goods中取
    all_list = []
    # 查看该表的所有数据,返回可迭代的queryset对象[obj1,obj2],用点大法取值
    all_types = GoodsType.objects.all()
    for _type in all_types:
        data = {}
        # 拼字典
        data['type'] = {'title': _type.title}
        data['good'] = []
        #用order_by将最新上架的商品排在最前面,取出前十个
        all_goods = _type.goods_set.filter(
            isActive=True).order_by('-create_time')[:10]
        for good in all_goods:
            d = {}
            d['title'] = good.title
            d['price'] = str(good.price)
            d['spec'] = good.spec
            # good.picture是个django的image对象
            d['picture'] = str(good.picture)
            data['good'].append(d)
        all_list.append(data)
    #将python中数据类型转为json串传输给前端
    return HttpResponse(json.dumps(all_list),
                        content_type='application/json')


















#响应前端的ajax
def check_register(request):
    # ajax的GET方式
    #检查用户名是否已注册
    #1.通过查询字符串的方式获取前端传来的用户名,和前端约定好该标签的name值:/index/check_register?username=xxx
    telephone = request.GET.get('telephone')
    #2检查数据库是否有该用户
    users = User.objects.filter(upthone=telephone)
    if users:
        # return HttpResponse('用户名已注册')
        return HttpResponse('1')
    return HttpResponse('0')

def check_username(request):

    username = request.GET.get('username')#这个username是通过前端ajax的url传过来的

    users = User.objects.filter(uname=username)


    if users:
        return HttpResponse('0')
    return HttpResponse('1')

def check_password(request):
    #判断密码
    username = request.GET.get('username')  # 这个username是通过前端ajax的url传过来的
    password = request.GET.get('password')  # 通过ajax传过来
    users = User.objects.filter(uname=username)
    if not password:
        return HttpResponse('1')#1表示密码为空
    elif users[0].password != password:
        return HttpResponse('0')#2用户名或密码错误
    else:
        return HttpResponseRedirect('index.html')#直接登录








