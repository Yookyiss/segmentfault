# -*- coding:utf-8 -*-
# @Time    : 2019/7/21 7:19 PM
# @Author  : __wutonghe__
# docs https://channels.readthedocs.io/en/latest/tutorial/part_3.html#rewrite-the-consumer-to-be-asynchronous


from channels.generic.websocket import AsyncWebsocketConsumer
import json


class AllNoticeConsumer(AsyncWebsocketConsumer):
    """
    私信websocket,采用异步通信来增加并发
    """

    async def connect(self):
        """当 websocket 一链接上以后触发该函数"""

        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add('notice-room',self.channel_name)  # create or enter聊天室
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """将答复交回给websocket"""
        await self.send(text_data=json.dumps(text_data))  # 将消息发送给前端

    async def disconnect(self, code):
        """断开链接时触发该函数"""

        await self.channel_layer.group_discard('notice-room',self.channel_name)  # exit 聊天室
