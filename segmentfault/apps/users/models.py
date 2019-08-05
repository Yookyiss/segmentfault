from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(verbose_name='昵称', blank=True, max_length=255)
    age = models.IntegerField(default=0, blank=True)
    city = models.CharField(max_length=255,null=True, blank=True)
    introduction = models.TextField(verbose_name='简介',blank=True, null=True)
    github = models.CharField(verbose_name='github地址',null=True,max_length=255, blank=True)
    create_time = models.DateField(verbose_name='注册时间',auto_now_add=True)
    picture = models.ImageField(verbose_name='头像',upload_to='profile_pics/', null=True, blank=True)
    company = models.CharField(max_length=255, blank=True)
    gain_votes = models.IntegerField(verbose_name='得票数',default=0)
    birthday = models.DateField(verbose_name='生日',null=True,blank=True)
    has_unread_notice = models.BooleanField(verbose_name='该用户有未读消息',default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username
