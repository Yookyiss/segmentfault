# -*- coding:utf-8 -*-
# @Time    : 2019/7/6 4:03 PM
# @Author  : __wutonghe__


from django.urls import path

from segmentfault.apps.qa.views import *

app_name = "qa"
urlpatterns = [
    # 创建问题
    path("create/",QuestionCreate.as_view(),name='create'),

    #分类查询问题
    path("new/",NewView.as_view(),name='new'),
    # path("subscribed/",Subscribed.as_view(),name='subscribed'),
    path("unanswered/",UnAnswered.as_view(),name='unanswerd'),
    path("hottest/",HotTest.as_view(),name='hottest'),
    # path("pay/",)

    #问题详情
    path("detail/<int:question_id>",QuestionDetail.as_view(),name='detail'),

    #发表回复
    path("reply/<int:question_id>",AnswerCreate.as_view(),name='reply'),

    #up or dowm
    path("vote/",votedquestion,name='votedquestion'),
    path("answer/vote/",votedanswer,name='votedanswer'),
    path("accept/",acceptanswer,name='acceptanswer'),

]
