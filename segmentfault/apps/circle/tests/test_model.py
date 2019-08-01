# -*- coding:utf-8 -*-
# @Time    : 2019/6/22 8:04 PM
# @Author  : __wutonghe__


from test_plus import TestCase


class TestCircleMessage(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(self.user,'testuser')

