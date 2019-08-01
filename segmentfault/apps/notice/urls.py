# -*- coding:utf-8 -*-
# @Time    : 2019/7/18 7:55 PM
# @Author  : __wutonghe__

from django.urls import path

from segmentfault.apps.notice.views import *

app_name = "notice"
urlpatterns = [
    path('all/',AllNoticeList.as_view(),name='all'),
    path('unread/',UnReadNoticeList.as_view(),name='unread'),
    path('light/',notice_light,name='light'),
    path('readall/',mark_read,name='readall'),

]
