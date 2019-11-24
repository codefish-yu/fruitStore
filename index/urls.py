from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/index
    url(r'^$',views.index),
    # http://127.0.0.1:8000/index/register
    url(r'^register',views.register),
    # http://127.0.0.1:8000/index/login
    url(r'^login', views.login),
    # http://127.0.0.1:8000/index/check_session
    url(r'^check_session', views.check_session),
    # http://127.0.0.1:8000/index/logout
    url(r'^logout', views.logout),
    # http://127.0.0.1:8000/index/load_goods
    url(r'^load_goods', views.load_goods)
]