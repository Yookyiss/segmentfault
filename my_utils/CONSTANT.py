# -*- coding:utf-8 -*-
# @Time    : 2019/7/6 1:45 PM
# @Author  : __wutonghe__


PRIVATE_FIRST_WORDS = '你好'  # 第一次发起私信时打招呼语句
NOTICE_TYPE = (
    ('L', '赞了'),
    ('A', '回答了'),
    ('W', '采纳了'),
    ('R', '回复了'),
    ('V', '投票了')
)
QA_TYPE = {
    '算法',
    '前端',
    '后端',
    '数据分析',
    '人工智能',
    'Android',
    'IOS',
    '程序员',
}

QA_RANK = 'qa_rank'  # 排行榜key
QA_DB = 11  # 问答模块redis库
QA_RANK_TOP_NUM = 10  # 排行榜显示数目

