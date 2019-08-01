from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse
from .models import *
from django.views.generic import ListView
from my_utils.decorator import ajax_login_requird
from django.views.decorators.http import require_http_methods
from segmentfault.apps.notice.views import post_notice

# Create your views here.


class CircleList(ListView):
    '''
    动态列表
    '''
    model = CircleMessage
    paginate_by = 5
    template_name = 'circle/circle_list.html'
    context_object_name = 'circle_list'
    ordering = ('like',)

    def get_queryset(self,**kwargs):
        return CircleMessage.objects.filter(is_comment=False,is_delete=False).select_related('user','parent')

    def get_context_data(self, *, object_list=None, **kwargs):

        kwargs['testob'] = CircleMessage.objects.all().first()
        return super().get_context_data(**kwargs)


@ajax_login_requird
@require_http_methods(["POST"])
def new_circle(request):
    '''
    发布动态接口
    :param request:
    :return:
    '''
    import uuid
    ob = CircleMessage.objects.create(uuid=uuid.uuid4(), user=request.user, context=request.POST.get('message').strip())

    return render(request, 'circle/circle_single.html', {"circle": ob})


@ajax_login_requird
@require_http_methods(["POST"])
def change_like(request):
    '''
    点赞取消赞接口
    :param request:
    :return:
    '''
    uuid = request.POST.get("uuid", '')
    ob = CircleMessage.objects.filter(uuid=uuid).first()
    if ob:
        res = ob.change_like(request.user)
        return JsonResponse({"status": 2000, "message": True, 'like_num': ob.get_like_num()})
    else:
        return JsonResponse({"status": 5000, "message": False})


@ajax_login_requird
@require_http_methods(["POST"])
def delete_circle(request):
    '''
    删除动态或评论接口
    :param request:
    :return:
    '''
    uuid = request.POST.get("uuid", '')
    ob = CircleMessage.objects.filter(uuid=uuid).first()
    ob.is_delete = True
    ob.save()
    return JsonResponse({'status': 2000, 'message': True})


@require_http_methods(["POST"])
def get_reply(request):
    '''
    评论列表接口
    :param request:
    :return:
    '''
    uuid = request.POST.get('uuid','')
    ob = CircleMessage.objects.filter(uuid=uuid).first()
    reply_num = ob.get_comment_num()
    reply_query = ob.get_comment(10)
    context = {
        'reply_list': reply_query,
        'reply_num':reply_num,
        'uuid':ob.uuid,
    }

    html_text = render_to_string("circle/circle_reply.html",context)
    return JsonResponse({"status":2000,"html_text":html_text})


@ajax_login_requird
@require_http_methods(["POST"])
def reply(request):
    '''
    发表回复接口
    :param request:
    :return:
    '''
    uuid = request.POST.get("uuid",'')
    text = request.POST.get('text','').strip()
    parent = CircleMessage.objects.filter(uuid=uuid).first()
    ob = CircleMessage.objects.create(user=request.user,context=text,parent=parent,is_comment=True)
    ob.save()
    post_notice(request.user,parent.user,'R',parent)  # 发送websocket通知
    return JsonResponse({"status":2000})


def test(request):
    from .tasks import app1
    a = app1.delay()
    return HttpResponse('ok')
