from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.shortcuts import redirect,reverse
from http import HTTPStatus


def home_redirect(request):
    """首页重定向"""
    return redirect(reverse('article:list'))

urlpatterns = [
    path("", home_redirect, name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('markdownx/', include('markdownx.urls')),  # 第三方包markdown路由配置
    path('search/',include('haystack.urls')),
    # User management
    path("circle/", include("segmentfault.apps.circle.urls", namespace="circle")),
    path("users/", include("segmentfault.apps.users.urls", namespace="users")),
    path("article/",include("segmentfault.apps.article.urls",namespace="article")),
    path("qa/",include("segmentfault.apps.qa.urls",namespace="qa")),
    path("accounts/", include("allauth.urls")),
    path("comments/",include("django_comments.urls")),
    path("msg/",include("segmentfault.apps.msg.urls",namespace='msg')),
    path("notice/",include("segmentfault.apps.notice.urls",namespace="notice")),


    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

def RESPONSE_500(request):
    return HTTPStatus(500)

handler500 = RESPONSE_500
