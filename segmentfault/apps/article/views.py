import datetime

from django.shortcuts import render,HttpResponse
from django.views.generic import ListView,UpdateView,CreateView,View,DetailView
from segmentfault.apps.article.forms import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from segmentfault.apps.article.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django_comments.signals import comment_was_posted
from segmentfault.apps.notice.views import post_notice


@method_decorator(cache_page(60*60*24),name='get')  # 缓存
class ArticleCreate(LoginRequiredMixin,CreateView):
    model = 'Article'
    template_name = 'article/article_add.html'
    form_class = ArticleForm

    def form_valid(self, form):
        """
        为文章添加作者
        :param form:
        :return:
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super(ArticleCreate, self).post(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy("article:list")


class ArticleList(ListView):
    """
    文章列表
    """
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'article_list'
    paginate_by = 4

    def get_queryset(self):
        article_list = Article.objects.filter(status='1')
        return article_list

    def get_context_data(self, *, object_list=None, **kwargs):
        # 返回最近定义的一段时间内的热门文章
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=100,hours=23, minutes=59, seconds=59)
        hot_article = self.model.objects.filter(create_time__gt=start).order_by('-click_num')[0:9]
        kwargs['hot_article'] = hot_article
        kwargs['pwd_page'] = 'article'

        return super(ArticleList, self).get_context_data(**kwargs)


class ArticleDetail(DetailView):
    """
    文章详情
    """
    model = Article
    template_name = 'article/article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetail, self).get_object()
        obj.click_num += 1  # 增加点击量
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        kwargs['article_type'] = 'xiangqing'
        return super().get_context_data(**kwargs)


class ArticleUpdate(LoginRequiredMixin,UpdateView):
    """
    更新文章
    """
    model = Article
    template_name = 'article/article_add.html'
    form_class = ArticleForm
    pk_url_kwarg = 'article_id'

    def get_success_url(self):
        #通过get_object()获取对象
        return reverse_lazy('article:detail',args=[self.get_object().id])


class ArticleDrafts(LoginRequiredMixin,ListView):
    """
    草稿箱
    """
    model = Article
    template_name = 'article/drafts.html'
    context_object_name = 'article_list'
    paginate_by = 4
    def get_queryset(self):
        article_list = Article.objects.filter(status='0',user=self.request.user)
        return article_list


def comment_signal(**kwargs):
    """信号函数"""
    sender = kwargs['request'].user
    instance = kwargs['comment'].content_object
    post_notice(sender,instance.user,'R',instance)


# https://django-contrib-comments.readthedocs.io/en/latest/signals.html#comment-was-posted
comment_was_posted.connect(receiver=comment_signal)  # django-comment-signal;
