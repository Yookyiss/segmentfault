# -*- coding:utf-8 -*-
# @Time    : 2019/6/26 4:47 PM
# @Author  : __wutonghe__

from django.urls import path
from django.views.decorators.cache import cache_page

from segmentfault.apps.article.views import *

app_name = "article"
urlpatterns = [
    path("list/",ArticleList.as_view(),name="list"),
    path("create/",ArticleCreate.as_view(),name='create'),
    path("detail/<int:article_id>",ArticleDetail.as_view(),name='detail'),
    path('update/<int:article_id>',ArticleUpdate.as_view(),name='update'),
    path("drafts/",ArticleDrafts.as_view(),name="drafts"),

]
