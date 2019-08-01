# -*- coding:utf-8 -*-
# @Time    : 2019/7/8 8:27 PM
# @Author  : __wutonghe__

from markdownx.fields import MarkdownxFormField
from django import forms
from segmentfault.apps.qa.models import Question,Answer


class QuestionForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ['title','is_draft','content']

class AnswerForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Answer
        fields = ['content',]

class Voted(forms.ModelForm):
    pass
