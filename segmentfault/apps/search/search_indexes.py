# -*- coding:utf-8 -*-
# @Time    : 2019/7/25 9:21 PM
# @Author  : __wutonghe__


from haystack import indexes


from segmentfault.apps.circle.models import CircleMessage
from segmentfault.apps.article.models import Article
from segmentfault.apps.qa.models import Question
from segmentfault.apps.users.models import User



class CircleMessageIndexes(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True,template_name='search/circle_text.txt')

    def get_model(self):
        return CircleMessage

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ArticleIndexes(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,template_name='search/article_text.txt') # 默认为template/search/indexes/,为了由于需求不高，这里改写一下

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class QuestionIndexes(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True,template_name='search/qa_text.txt')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserIndexes(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True,template_name='search/user_text.txt')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
