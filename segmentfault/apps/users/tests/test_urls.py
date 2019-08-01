# -*- coding:utf-8 -*-
# __author__ = "__wutonghe__"


from test_plus.test import TestCase
from django.urls import reverse,resolve

class TestUrl(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'),'/users/update/')
