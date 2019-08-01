[django-markdownx文档地址](https://neutronx.github.io/django-markdownx/)

#####简单使用：
```
1.在models中使用 MarkdownxField模型字段
2.在urls中添加接口
3.在form表单中添加content = MarkdownxFormField()
4.可以在template/markdownx 新建widgit2.html用于重写返回
  渲染后的markdown模版，可在widgit2.html中使用bootstarp
  在前端使用crispy进行django过滤
5.一旦使用了自定义的widgit，那么需要修改django默认的模版渲染引擎


```
