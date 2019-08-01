from django.shortcuts import render,HttpResponse
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from my_utils.decorator import ajax_login_requird
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from segmentfault.apps.msg.models import Message
from segmentfault.apps.users.models import User


class MessageList(LoginRequiredMixin,ListView):
    model = Message
    template_name = 'message/message_privateletter.html'
    context_object_name = "message_list"

    def get_queryset(self):
        """
        返回所有聊天用户
        :return:
        """
        return []

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        获取所有私信对象
        :param object_list:
        :param kwargs:
        :return:
        """
        set1 = self.model.objects.filter(sender=self.request.user).select_related('sender', 'recipient')
        set2 = self.model.objects.filter(recipient=self.request.user).select_related('sender', 'recipient')
        all_private_users = set()
        for vo in set1:
            all_private_users.add(vo.recipient)
        for vo in set2:
            all_private_users.add(vo.sender)
        kwargs['all_users'] = all_private_users  # 获取所有私信对象
        return super().get_context_data(**kwargs)



class MessageDetail(MessageList):
    """
    返回聊天记录
    """
    def get_queryset(self):
        message_list = self.model.objects.get_conversation(self.request.user,self.kwargs['user_id'])

        if not message_list:  # 当第一次发起私信的时候，隐式的创建一个message
            recipient = User.objects.filter(id=self.kwargs['user_id']).first()
            from my_utils.CONSTANT import PRIVATE_FIRST_WORDS  # 初始打招呼语句
            ob = Message.objects.create(sender=self.request.user,recipient=recipient,message=PRIVATE_FIRST_WORDS)
            message_list = [ob]

        return message_list

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['recipient'] = int(self.kwargs['user_id'])
        return super().get_context_data(**kwargs)



def create_data(request):
    user = User.objects.get(id=2)
    ob = Message.objects.create(message='byebye',sender=request.user,recipient=user,)
    return HttpResponse('ok')


@ajax_login_requird
@require_http_methods(["POST"])
def post_letter(request):
    recipient = request.POST.get('recipient')
    message = request.POST.get('message')
    if not recipient:
        return JsonResponse({'status':5000,'msg':'请选择一个好友之后再发送'})

    from segmentfault.apps.users.models import User
    r_user = User.objects.filter(id=recipient).first()  # 接收者
    ob = Message.objects.create(sender=request.user,recipient=r_user,message=message)  # 生成新聊天记录
    context = {'message': ob}
    htmlslice = render_to_string('message/messafe_singleletter.html', context)  # html代码片

    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    kwargs = {
        'type':'receive',
        'message':htmlslice,
        'sender':request.user.username
    }  # kwargs即是前端接受到的event.data

    from asgiref.sync import async_to_sync
    async_to_sync(channel_layer.group_send)(r_user.username+'-message', kwargs)  # 把消息发送到聊天室（频道）
    return JsonResponse({'status':2000,'htmlslice':htmlslice})
