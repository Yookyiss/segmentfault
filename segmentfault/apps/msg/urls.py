# -*- coding:utf-8 -*-
# @Time    : 2019/7/18 7:55 PM
# @Author  : __wutonghe__


from django.urls import path

from segmentfault.apps.msg.views import *

app_name = "msg"
urlpatterns = [
    path("createdata/",create_data),
    path("allletter/",MessageList.as_view(),name="allletter"),
    path("letter/<str:user_id>",MessageDetail.as_view(),name='letter'),
    path("post-letter/",post_letter,name='post_letter'),

]
