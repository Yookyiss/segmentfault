from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView,ListView
from django.shortcuts import render

from segmentfault.apps.users.models import User

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username" #查询的时候以此字段做查询
    slug_url_kwarg = "username" #从url中接受username参数
    template_name = 'users/user_detail.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name","age","city","introduction","github","picture","company",'birthday']
    template_name = 'users/user_form.html'
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserList(LoginRequiredMixin,ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'user_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['test'] = 1
        return super(UserList, self).get_context_data(**kwargs)
