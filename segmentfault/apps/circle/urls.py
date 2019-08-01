# -*- coding:utf-8 -*-
# @Time    : 2019/6/22 8:18 PM
# @Author  : __wutonghe__



from django.urls import path

from segmentfault.apps.circle.views import *
app_name = "circle"
urlpatterns = [
    path("list/", view=CircleList.as_view(), name="list"),
    path("new/",view=new_circle,name="new"),
    path("like/",view=change_like,name="like"),
    path("delete/",view=delete_circle,name='delete'),
    path("getreply/",view=get_reply,name='getreply'),
    path("reply/",view=reply,name='reply'),
    path("test/",view=test,name='test')

]
