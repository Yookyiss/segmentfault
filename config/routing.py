# -*- coding:utf-8 -*-
# @Time    : 2019/7/21 12:57 PM
# @Author  : __wutonghe__


from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # 集成django auth
from channels.security.websocket import AllowedHostsOriginValidator  # 授权的ip或域名

from segmentfault.apps.msg.consumer import MessageConsumer
from segmentfault.apps.notice.consumer import AllNoticeConsumer


application = ProtocolTypeRouter({

    # WebSocket message handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/notice/',AllNoticeConsumer),  # 此匹配必须放在前面，不然会优先匹配<str:name>
                path('ws/<str:username>/', MessageConsumer),  # 私信websocket routing


            ])
    )),
    # Using the third-party project frequensgi, which provides an APRS protocol
})
