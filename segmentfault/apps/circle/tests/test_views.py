# -*- coding:utf-8 -*-
# @Time    : 2019/6/22 7:55 PM
# @Author  : __wutonghe__

from test_plus.test import TestCase
from django.test import RequestFactory
from segmentfault.apps.circle.views import *
class BaseUser(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory


