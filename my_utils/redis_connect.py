# -*- coding:utf-8 -*-
# @Time    : 2019/7/23 12:50 PM
# @Author  : __wutonghe__

import redis
from config.settings.base import REDIS_HOST
REDIS_HOST = ':'.join(REDIS_HOST.split(':')[1:-1])[2:] # 获取host


class RedisConnect(object):
    def __init__(self,db=0):
        pool = redis.ConnectionPool(host=REDIS_HOST,port=6379,db=db,decode_responses=True)
        self._r = redis.Redis(connection_pool=pool)

    @property
    def redis(self):
        return self._r
