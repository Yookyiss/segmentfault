from collections import Counter

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation,GenericForeignKey
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
from django.urls import reverse


from segmentfault.apps.users.models import User


class Vote(models.Model):
    """
    投票表
    """
    user = models.ForeignKey(User,verbose_name='投票者',related_name='vote',on_delete=models.CASCADE)
    opinion = models.BooleanField(default=True,verbose_name='投票意见')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='最后修改时间',auto_now=True)

    # 此字段在数据表不存在,用于协助下面两个字段进行各类操作
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    # 定位对象的id
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # 外键所指对象的model 在django_content_type表中的id
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.opinion


class QuestionQuerySet(models.query.QuerySet):
    """
    问题查询管理器
    """

    def get_hasaccept(self):
        pass

    def get_noneaccept(self):
        pass


class Question(models.Model):

    """
    问题表
    """
    user = models.ForeignKey(User,related_name="question",on_delete=models.CASCADE,verbose_name='问题提问者')
    title = models.CharField(max_length=255,verbose_name='标题')
    is_draft = models.BooleanField(default=True,verbose_name='是否是草稿')
    status = models.CharField(max_length=10,choices=(('open','开启'),('close','关闭')),default='open')
    # image = models.ImageField(verbose_name='问题图片',upload_to='qa/%Y/%m/%d/',null=True)
    content = MarkdownxField(verbose_name='内容')
    has_accept = models.BooleanField(default=False,verbose_name='回答已接受')
    tags = TaggableManager(verbose_name='标签',help_text='wait a moment',blank=True)
    votes = GenericRelation(Vote,verbose_name='投票')
    visited_num = models.IntegerField(verbose_name='浏览量',default=0)

    create_time = models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='最后更新时间')

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdownify(self.content)

    def get_votes(self):
        hashmap = Counter(self.votes.values_list('opinion',flat=True))
        res = hashmap[True] - hashmap[False]
        return res if res >=0 else 0

    def get_answernum(self):
        return self.answer_set.count()

    def get_simplecontent(self):
        if len(self.content) > 20:
            return self.content[0:20] + '...'
        return self.content

    def get_users(self):
        users = self.votes.values_list('user',flat=True)
        return users

    def get_abspath(self):
        return reverse("qa:detail", kwargs={"question_id": self.id})

class Answer(models.Model):
    user = models.ForeignKey(User,related_name="answer",on_delete=models.CASCADE,verbose_name='回答者')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name='问题')
    content = MarkdownxField(verbose_name='回答内容',null=True)
    is_accept = models.BooleanField(verbose_name='被接受',default=False)
    votes = GenericRelation(Vote,verbose_name="得票")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='最后修改时间')

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = verbose_name
        ordering = ("-is_accept","-update_time") #如果被采纳即在前端置顶

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def get_upvote_users(self):
        return self.votes.filter(opinion=True).values_list('user',flat=True)

    def get_downvote_users(self):
        return self.votes.filter(opinion=False).values_list('user',flat=True)

    def get_votes(self):
        hashmap = Counter(self.votes.values_list('opinion',flat=True))
        res = hashmap[True] - hashmap[False]
        return res if res >=0 else 0
