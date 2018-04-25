#!usr/bin/python
# -*- coding: utf-8 -*-
'''
工具类  ---  那些需要重复使用的代码块
'''
import re
import FuleiHeader
import LoginFulei

class FuleiTool(object):
    def __init__(self):
        pass

    @staticmethod
    def getHash(htm):
        hash_pattern = re.compile(r'<input type="hidden" name="__hash__" value="(.*?)"')
        _hash = re.findall(hash_pattern,htm)[0]
        return _hash

    '''
    得到机器的某个时间段的合计金额,合计次数
    startTime与endTime是时间戳格式
    服务器会返回[次数，金额]
    '''
    @staticmethod
    def getMoney(eid, startTime, endTime):
        url = "http://www.kadawo.com/fulei/index.php/equipment/hjslAjax"
        header = FuleiHeader.FuleiHeader.postHjsl()
        login = LoginFulei.LoginFulei()
        header.setdefault('Cookie', 'PHPSESSID=%s' % login.getCookie())
        post_data = "did="+eid+"&startTime="+startTime+"&endTime="+endTime
        result = LoginFulei.LoginFulei.session.post(url,data=post_data,headers=header)
        return result.text.strip('[]').split(',')