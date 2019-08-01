from django.shortcuts import render
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from segmentfault.apps.qa.models import *
from .forms import QuestionForm,AnswerForm
from my_utils.decorator import ajax_login_requird
from django.views.decorators.http import require_http_methods
from segmentfault.apps.notice.views import post_notice
from my_utils.redis_connect import RedisConnect
from my_utils.CONSTANT import QA_RANK,QA_DB,QA_RANK_TOP_NUM

r = RedisConnect(db=QA_DB).redis

# Create your views here.


class QuestionBaseView(ListView):
    """
    问题基类
    """
    # model = Question
    queryset = Question.objects.select_related('user') #orm查询优化，可显著减少sql语句查询数量
    template_name = 'qa/qa_list.html'
    context_object_name = "questions_list"
    question_type = 'new' #自定义字段，供get_context_data使用
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['active'] = self.question_type
        kwargs['rank'] = r.zrevrange(QA_RANK,0,QA_RANK_TOP_NUM-1,withscores=True)

        return super().get_context_data(**kwargs)


class NewView(QuestionBaseView):
    """
    最新问答
    """
    question_type = 'new'

    def get_queryset(self):
        return Question.objects.filter(status='open').order_by('-create_time').select_related('user')

#
# class Subscribed(QuestionBaseView):
#     """
#     为我推送
#     """
#     question_type = 'subscribed'
#
#     def get_queryset(self):
#         return Question.objects.all().order_by('answer')


@method_decorator(cache_page(60),name='get')
class UnAnswered(QuestionBaseView):
    """
    等待回答
    """
    question_type = 'unanswered'

    def get_queryset(self):
        return Question.objects.filter(has_accept=False)


@method_decorator(cache_page(60*60),name='get')
class HotTest(QuestionBaseView):
    """
    热门问答
    """
    question_type = 'hottest'

    def get_queryset(self):
        return Question.objects.all().order_by('-visited_num')


class PayQuestion(QuestionBaseView):
    """
    付费问答
    """
    pass


@method_decorator(cache_page(60*60*24),name='get')
class QuestionCreate(LoginRequiredMixin,CreateView):
    """
    创建提问
    """
    form_class = QuestionForm
    template_name = 'qa/qa_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("qa:new")


class QuestionDetail(DetailView):
    """
    问题详情
    """
    model = Question
    context_object_name = 'question'
    template_name = 'qa/qa_detail.html'
    pk_url_kwarg = 'question_id'

    def get_object(self, queryset=None):
        """增加浏览量"""
        question = Question.objects.filter(id=self.kwargs['question_id']).first()
        question.visited_num += 1
        question.save()
        return super().get_object()

    def get_context_data(self, **kwargs):
        kwargs['answer_list'] = kwargs['object'].answer_set.all().select_related('user') # detaillist中的查询对象名为object
        if self.request.user.id in self.object.get_users():
            user_vote = self.object.votes.filter(user=self.request.user).first()
            kwargs["user_vote"] = 1 if user_vote.opinion else 0
        else:
            kwargs["user_vote"] = -1 # user_vote是该用户对问题的投票信息

        return super().get_context_data(**kwargs)


@method_decorator(cache_page(60*60*24),name='get')
class AnswerCreate(LoginRequiredMixin,CreateView):
    """
    发表回答
    """
    template_name = 'qa/qa_answer_create.html'
    form_class = AnswerForm
    pk_url_kwarg = 'question_id'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.request.POST.get('question_id')
        return super().form_valid(form)

    def get_success_url(self):
        # websocket 通知
        instance = Question.objects.filter(id=self.request.POST.get('question_id')).first()
        recipient = instance.user
        post_notice(self.request.user,recipient,'A',instance)
        return reverse_lazy("qa:detail",args=[self.request.POST.get('question_id')])

    def get_context_data(self, **kwargs):
        kwargs['question_id'] = self.kwargs['question_id'] #self.kwargs中记录着路由参数的信息
        return super().get_context_data(**kwargs)


@ajax_login_requird
@require_http_methods(["POST"])
def votedquestion(request):
    """
    给问题投票
    :param request:
    :return:
    """
    qa_id = request.POST.get('id','')
    vo = request.POST.get('vote','')
    question = Question.objects.filter(id=qa_id).first()
    users = question.votes.values_list('user',flat=True)
    if request.user.id in users:
        if vo == 'neutral':
            question.votes.get(user=request.user).delete()
        else:
            vo = True if vo == 'up' else False
            question.votes.update(user=request.user, opinion=vo)
    else:
        vo = True if vo == 'up' else False
        question.votes.create(user=request.user,opinion=vo)

    return JsonResponse({'status':2000,'vote_num':question.get_votes()})

@ajax_login_requird
@require_http_methods(["POST"])
def votedanswer(request):
    """
    给回答投票
    :param request:
    :return:
    """
    answer_id = request.POST.get('id','')
    vo = request.POST.get('vote','')
    answer = Answer.objects.filter(id=answer_id).first()
    users = answer.votes.values_list('user', flat=True)
    if request.user.id in users:
        if vo == 'neutral':
            answer.votes.get(user=request.user).delete()
        else:
            vo = True if vo == 'up' else False
            answer.votes.update(user=request.user, opinion=vo)
            post_notice(request.user, answer.user,'V',answer)  # websocket
    else:
        vo = True if vo == 'up' else False
        answer.votes.create(user=request.user, opinion=vo)
        post_notice(request.user, answer.user, 'V', answer)  # websocket

    return JsonResponse({'status': 2000, 'vote_num': answer.get_votes()})

@ajax_login_requird
@require_http_methods(["POST"])
def acceptanswer(request):
    """
    采纳问题
    :param request:
    :return:
    """
    answer_id = request.POST.get('answer_id')
    answer = Answer.objects.filter(id=answer_id).first()
    if request.user != answer.question.user and request.user != answer.user:  # 保证采纳人一定是问题的提问者,而且不能自己采纳自己
        return JsonResponse({'status': 4003, 'msg': '非法操作'})
    answer.is_accept = True

    if not answer.question.has_accept:
        answer.question.has_accept = True
    else:
        return JsonResponse({'status': 4003, 'msg': '非法操作'})
    answer.question.save()
    answer.save()

    # websocket 发送
    recipient = answer.user
    sender = answer.question.user
    instance = answer
    post_notice(sender,recipient,'W',instance)

    # 更新排行榜
    r.zincrby(QA_RANK,int(1),answer.user.name)

    return JsonResponse({'status': 2000, 'msg': 'ok'})















