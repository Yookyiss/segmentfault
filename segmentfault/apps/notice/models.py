import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from segmentfault.apps.users.models import User

# Create your models here.


class Notice(models.Model):
    from my_utils.CONSTANT import NOTICE_TYPE

    uuid_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    # 使用related_name关联是因为有两个字段同时关联User
    sender = models.ForeignKey(User,related_name='n_sender_user',on_delete=models.CASCADE,verbose_name='消息发送者')
    recipient = models.ForeignKey(User,related_name='n_recipient_user',on_delete=models.CASCADE,verbose_name='消息接受者')

    is_read = models.BooleanField(verbose_name='是否已读',default=False,db_index=True)
    verb = models.CharField(verbose_name='通知类别',choices=NOTICE_TYPE,max_length=1)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True,db_index=True)

    # 此字段在数据表不存在,用于协助下面两个字段进行各类操作
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    # 定位对象的id
    object_id = models.PositiveIntegerField(blank=True, null=True)
    # 外键所指对象的model 在django_content_type表中的id
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

    @classmethod
    def read_all(cls,recipient):
        if recipient:
            cls.objects.filter(recipient=recipient).update(is_read=True)

    @classmethod
    def has_unread(cls,self):
        """
        用于显示主页的消息指示灯闪亮
        :param self:
        :return:
        """
        if cls.objects.filter(is_read=False):
            return True
        return False
