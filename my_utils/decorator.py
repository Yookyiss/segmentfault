# -*- coding:utf-8 -*-
# @Time    : 2019/6/25 3:44 PM
# @Author  : __wutonghe__

from django.http import HttpResponse,JsonResponse
from functools import wraps


def ajax_login_requird(func):
    @wraps(func)
    def new_func(request):
        if request.user.is_authenticated:
            return func(request)
        else:
            return JsonResponse({"status":3002,"message":"no_login"})
    return new_func

