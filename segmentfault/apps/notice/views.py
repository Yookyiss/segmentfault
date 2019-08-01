from django.shortcuts import render,reverse,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from asgiref.sync import async_to_sync
from django.http.response import JsonResponse
from channels.layers import get_channel_layer
from segmentfault.apps.notice.models import Notice
from segmentfault.apps.users.models import User
# Create your views here.


class AllNoticeList(ListView):
    """
    所有消息
    """
    model = Notice
    template_name = 'notice/notice_list.html'
    context_object_name = 'notice_list'
    paginate_by = 10
    
    def get_queryset(self):
        return self.model.objects.filter(recipient=self.request.user)


class UnReadNoticeList(AllNoticeList):
    """
    未读消息
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)


def post_notice(sender,recipient,verb,content_object):
    """
    websocket 消息发送函数

    :param sender: 发送者
    :param recipient: 接收者
    :param verb: 类型
    :param content_object:具体实例
    :return:
    """
    Notice.objects.create(
        sender=sender,
        recipient=recipient,
        verb=verb,
        content_object=content_object,  # 手动指定与消息有关的实例，无需通过外键创建
    )

    recipient.has_unread_notice = True  # 该用户有未读消息
    recipient.save()

    channel_layer = get_channel_layer()
    kwargs = {
        'type':'receive',  # 必填字段 必须是receive
        'sender':sender.name,
        'message':'message coming'
    }
    async_to_sync(channel_layer.group_send)('notice-room',kwargs)  # 异步变同步


def notice_light(request):
    """是否有未读通知"""

    if Notice.objects.filter(is_read=False,recipient=request.user):
        return JsonResponse({'status':2000,'msg':True})  # 该用户有未读消息
    return JsonResponse({'status':2000,'msg':False})  # 无未读消息


def mark_read(request):
    """全部标记已读"""
    Notice.read_all(request.user)
    request.user.has_unread_notice = False  # 将有未读消息置为False
    request.user.save()
    return redirect(reverse('notice:all'))
