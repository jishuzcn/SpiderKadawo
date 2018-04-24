#!/usr/bin/python
# -*- coding: utf-8
'''
爬取彩票机首页数据
1.得到Session会话对象
2.用BeautifulSoup4爬取页面数据
3.get下一页并爬取数据
...
'''
__Author__ = '汪思源'
__Vision__ = 0.1
__Date__ = '2018.4.24 16/47'

from LoginFulei import *
from FuleiHeader import *
from bs4 import BeautifulSoup

class SpiderIndex(object):
    #唯一会话id
    login = LoginFulei()
    session = login.session

    def __init__(self):
        if not SpiderIndex.login.isLogin():
            SpiderIndex.login.doLogin()

    def getHtml(self):
        header = FuleiHeader.getshjList()
        header.setdefault('Cookie','PHPSESSID=%s' % SpiderIndex.login.getCookie())
        htm = self.session.get(r"http://www.kadawo.com/fulei/index.php/equipment/shjList",headers = header,allow_redirects=False)
        return htm

if __name__ == '__main__':
    spiner = SpiderIndex()
    # spiner.getHtml()
