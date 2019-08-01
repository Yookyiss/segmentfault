# -*- coding:utf-8 -*-
# __author__ = "__wutonghe__"

from django.db import models

# Create your models here.
from segmentfault.apps.users.models import User
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.urls import reverse



class ArticleQuerySet(models.query.QuerySet):
    """
    query管理器
    """
    def get_published(self):
        #select_related通过多表join关联查询，一次性获得所有数据，通过降低数据库查询次数来提升性能
        return self.filter(status=1).select_related('user')

    def get_draft(self):

        return self.filter(status=0).select_related('user')





class Article(models.Model):
    '''
    文章表
    '''

    title = models.CharField(max_length=255,verbose_name='标题')
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,verbose_name='作者')
    image = models.ImageField(upload_to='article/%Y/%m/%d/',verbose_name='图片')
    status = models.CharField(max_length=1,choices=(('1','发布'),('0','草稿')),default=0,verbose_name='文章状态')
    content = MarkdownxField(verbose_name='内容')
    is_edit = models.BooleanField(verbose_name='可以编辑',default=False)
    create_time = models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='最后更新时间')
    click_num = models.IntegerField(verbose_name='点击量',default=0)
    types = models.CharField(max_length=255,verbose_name='文章类型',choices=(('yc','原创'),('fy','翻译'),('zz','转载')),null=True)
    #重写query管理器
    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('create_time',)

    def __str__(self):
        return self.title

    def get_makdown_html(self):
        return markdownify(self.content)

    def get_abspath(self):
        return reverse("article:detail", kwargs={"article_id": self.id})
