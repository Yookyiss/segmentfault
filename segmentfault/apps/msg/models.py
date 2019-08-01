from django.db import models
from segmentfault.apps.users.models import User
# Create your models here.


class MessageQuerySet(models.query.QuerySet):
    def get_conversation(self,sender,recipient):
        """
        返回聊天记录
        :param sender:
        :param recipient:
        :return:
        """
        set1 = self.filter(sender=sender,recipient=recipient).select_related('sender','recipient')  # 使用select_related进行join连表查询，减少sql查询次数
        set2 = self.filter(sender=recipient,recipient=sender).select_related('sender','recipient')
        return set1.union(set2).order_by('create_time')  # 按时间顺序排列



class Message(models.Model):
    sender = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='发送者',related_name='sender_user')
    recipient = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='接收者',related_name='recipient_user')
    message = models.TextField(verbose_name="内容")
    is_read = models.BooleanField(default=False,verbose_name="是否已读")
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    objects = MessageQuerySet.as_manager()


    class Meta:
        verbose_name = "私信"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message

    def read(self):
        self.read = True
        self.save()
