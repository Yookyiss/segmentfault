from markdownx.fields import MarkdownxFormField
from django import forms
from segmentfault.apps.article.models import Article


class ArticleForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Article
        fields = ['title','image','status','content',]

