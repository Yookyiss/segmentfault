# -*- coding:utf-8 -*-
# __author__ = "__wutonghe__"

import uuid


from django.db import models

from segmentfault.apps.users.models import User
from segmentfault.apps.notice.views import post_notice

# Create your models here.



class CircleMessage(models.Model):
    """
    一张表解决动态和其评论
    """
    uuid = models.UUIDField(unique=True,default=uuid.uuid4,editable=False)
    #当用户被删除后，该表外键置空
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,
                             related_name='message_user',verbose_name='用户')
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE,
                               related_name='message_parent',verbose_name='自关联')
    context = models.TextField(verbose_name='内容')
    like = models.ManyToManyField(User,verbose_name='点赞用户')
    is_comment = models.BooleanField(default=False,verbose_name='是否是评论')
    create_time = models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')
    edit_time = models.DateTimeField(auto_now=True,verbose_name='最后修改时间')
    is_delete = models.BooleanField(default=False,verbose_name='是否已经删除')

    class Meta:
        verbose_name = '动态与评论表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.context

    def change_like(self,user):
        """
        对赞进行更改
        :param user: 操作用户昵称name
        :return: 操作结果
        """
        if user in self.like.all():
            self.like.remove(user)
        else:
            self.like.add(user)
            post_notice(user,self.user,'L',self)
        return True

    def get_parent(self):
        """
        获取父级别或者自己
        :return:
        """
        if self.parent:
            return self.parent
        return self

    def get_like_num(self):
        """
        获取点赞人数
        :return:
        """
        return self.like.count()

    def get_like_people(self):
        """
        获取点赞人
        :return:
        """
        return self.like.all()

    def get_comment_num(self):
        """
        获取当前动态或者评论的评论数
        :return:
        """
        return self.message_parent.filter(is_delete=False).count()

    def get_comment(self,num):
        """
        获取当前动态或者评论的评论
        :return:
        """
        return self.message_parent.filter(is_delete=False).select_related('user')[0:num]

    def get_same_level_comment(self):
        """
        获取同一级的评论
        :return:
        """
        parent = self.get_parent()
        return parent.message_parent.all()

    def reply_message(self,user,context):
        parent = self.get_parent()
        CircleMessage.objects.create(
            user=user,
            parent=parent,
            is_comment=True,
            context=context,
        )

    def save(self,*args,**kwargs):
        super(CircleMessage,self).save(*args,**kwargs)


