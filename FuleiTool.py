#!usr/bin/python
# -*- coding: utf-8 -*-
'''
工具类  ---  那些需要重复使用的代码块
'''
import re
import FuleiHeader
import LoginFulei
import time
import os

class FuleiTool(object):
    def __init__(self):
        pass

    @staticmethod
    def getHash(htm):
        hash_pattern = re.compile(r'<input type="hidden" name="__hash__" value="(.*?)"')
        _hash = re.findall(hash_pattern,htm)[0]
        return _hash

    # tim = '2018-04-25'
    @staticmethod
    def timeToTimestamp(tim):
        # 转换成时间数组
        timeArray = time.strptime(tim,"%Y-%m-%d")
        # 转换成时间戳
        return int(time.mktime(timeArray))

    #得到当天0点的时间戳
    @staticmethod
    def getStartTimeOfToday():
        t = time.localtime(time.time())
        return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S')))

    #得到当天23点59的时间戳
    @staticmethod
    def getEndTimeOfToday():
        t = time.localtime(time.time())
        return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 23:59:59', t),'%Y-%m-%d %H:%M:%S')))

    '''
    因为后台要用'/'作为传输的分隔符，所以要转换一下url链接
    把所有'?'、'='、'&'符转换为'/'
    '''
    @staticmethod
    def urlReplace(url):
        if not url.find('?') == -1:
            url = url.replace('?','/')
        if not url.find('=') == -1:
            url = url.replace('=','/')
        if not url.find('&') == -1:
            url = url.replace('&','/')
        return url
