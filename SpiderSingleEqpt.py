#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
爬取单一设备的详细信息
Eqpt : Equipment
1.得到login对象并获取到唯一Session值
2.完全模拟浏览器请求行为，获取到FuleiHeader头部信息
3.爬取需要的数据
"""
__Author__ = '汪思源'
__Vision__ = 0.1
__Date__ = '2018.4.27 11:08'

import LoginFulei
import FuleiHeader
import FuleiTool
from bs4 import BeautifulSoup


class SpiderSingleEqpt(object):
    # 唯一会话id
    login = LoginFulei.LoginFulei()
    flheader = FuleiHeader.FuleiHeader()
    session = login.session
    fltool = FuleiTool.FuleiTool()

    def __init__(self, id):
        """
        :param id:设备编号
        """
        self.id = id
        if not self.login.isLogin():
            self.login.doLogin()

    def get_html(self,url):
        """
        得到当前设备的html信息
        :return:
        """
        header = self.flheader.getSingle()
        header.setdefault("Cookie", 'PHPSESSID=%s' % LoginFulei.LoginFulei.getCookie())
        htm = self.session.get(url,headers = header,allow_redirects=False)
        return htm.text

    def get_lottery_name(self):
        """
        得到彩票机里存放的彩票种类名
        :return: str字符串
        """
        url = self.generate_url(True,type='eType1')
        htm = self.get_html(url)
        soup = BeautifulSoup(htm,"lxml")
        # tbody = soup.find("tbody")
        return soup.tbody.tr.findAll('td')[5].text

    def get_iae_online(self,startTime,endTime,e_hash):
        """
        得到在线收支 iae : income and expenses
        :param e_hash: 页面的hash值，链接需要带着这个参数GET到数据
        :param startTime:开始时间，str类型，如:2018-4-1
        :param endTime:结束时间，str类型，如:2018-4-1
        :return:
        """

        pass

    def generate_url(self,single=False,**kwargs):
        """
        warning!!! 如果不是访问首页必须要传startTime与endTime
        :param kwargs: type,szType,startTime,endTime,__hash__,
              type = signIn、eType1、refund、eType1information
        :return: str
        首页
        eType1/id/571/__hash__/hash/
        首页条件查询
        eType1/id/571/startTime/2018-03-01/endTime/2018-04-01/__hash__/hash/
        出货详情
        refund/id/571/startTime/2018-03-01/endTime/2018-04-01/__hash__/hash/
        现金收支
        eType1information/id/571/szType/xj/startTime/2018-03-01/endTime/2018-04-01/__hash__/hash/
        在线收支
        eType1information/id/571/szType/zx/startTime/2018-03-01/endTime/2018-04-01/__hash__/hash/
        """
        url = "http://www.kadawo.com/fulei/index.php/equipment/"
        if single is True:
            url = url + kwargs['type'] + "/id/" + self.id +"/"
        elif 'szType' in kwargs.keys():
            url = url + kwargs['type'] + "/id/" + self.id +"/szType/" + kwargs['szType'] +\
                  "/startTime/"+kwargs['startTime']+"/endTime/"+kwargs['endTime']+"/__hash__/"+kwargs['hash']+"/"
        else:
            url = url + kwargs['type'] + "/id/" + kwargs['id'] +"/startTime/"+kwargs['startTime']+\
                  "/endTime/"+kwargs['endTime']+"/__hash__/"+kwargs['hash']+"/"

        return url

if __name__ == '__main__':
    single = SpiderSingleEqpt('998')
    # print(single.login.isLogin())
    print(single.get_lottery_name())

