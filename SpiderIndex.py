#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
爬取彩票机数据
1.得到唯一Session会话对象
2.用BeautifulSoup4爬取页面数据
3.get下一页并爬取数据
...
'''
__Author__ = '汪思源'
__Vision__ = 0.1
__Date__ = '2018.4.24 16:47'

from bs4 import BeautifulSoup
import LoginFulei
import FuleiHeader
import re
import FuleiTool
import furl
import time
import requests


class SpiderIndex(object):
    # 唯一会话id
    login = LoginFulei.LoginFulei()
    flheader = FuleiHeader.FuleiHeader()
    fltool = FuleiTool.FuleiTool()
    session = login.session

    def __init__(self):
        # self.htm = self.getHtml() # 默认得到彩票机首页信息
        # # 因为只是获取数据，不是修改，可以用一个BeautifulSoup实例
        # self.soup = BeautifulSoup(htm, "lxml")
        if not SpiderIndex.login.isLogin():
            SpiderIndex.login.doLogin()

    def getHtml(self, url=None):
        """
        得到某一页的Html信息
        :param url: url链接
        :return: html文本信息
        """
        header = SpiderIndex.flheader.getshjList()
        header.setdefault('Cookie', 'PHPSESSID=%s' % SpiderIndex.login.getCookie())
        global htm
        if url is None:
            try:
                htm = self.session.get(r"http://www.kadawo.com/fulei/index.php/equipment/shjList", headers=header,
                                       allow_redirects=False)
            except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
                # logging.error("There is a error: %s" % e)
                print("error")
        else:
            try:
                htm = self.session.get(url, headers=header, allow_redirects=False)
            except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
                # logging.error("There is a error: %s" % e)
                print("error")
        return htm.text

    # def writeContent(self):
    #     global soup
    #     table = soup.find("table")
    #     with open(r"/fuleiContent.txt", 'ab') as f:
    #         for tr in table.findAll('tr'):
    #             for th in tr.findAll('th'):
    #                 with open(r"/fuleiContent.txt", 'ab') as fth:
    #                     fth.write(th.getText().encode('utf-8'))
    #                     fth.write("\n".encode('utf-8'))
    #             for td in tr.findAll('td'):
    #                 with open(r"/fuleiContent.txt", 'ab') as ftd:
    #                     ftd.write(td.getText().encode('utf-8'))
    #                     ftd.write("\n".encode('utf-8'))

    def getTotalPage(self, htm):
        """
        :param htm:
        :return: 返回总页数
        """
        total_page_pattern = re.compile(r"1/(.*?) 页")
        total = re.findall(total_page_pattern, htm)
        return total[0]

    def getIndexData(self, htm, startTime=None, endTime=None):
        """
        得到某一页的数据
        序号(nid)2 设备ID(eid)3 设备名称(ename)4 设备地址(eaddress)5 持有人(holder)8
        所属(bto)9 合计次数(ttimes) 合计金额(tmoney) 库存(stock)12 运行状态(status)13
        :param soup:BeautifulSoup对象
        :param startTime:开始时间,类型为TimeStamp
        :param endTime:开始时间,类型为TimeStamp
        :return d = [{'nid':'01','eid':'868201049..',...},{....}]
        """
        if not startTime:
            startTime = self.fltool.getStartTimeOfToday()
        if not endTime:
            endTime = self.fltool.getEndTimeOfToday()
        data = []
        soup = BeautifulSoup(htm, "lxml")
        tbody = soup.find("tbody")
        rows = tbody.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            da = {}
            # cols = [ele.text.strip() for ele in cols]
            # print(cols)
            # data.append([ele for ele in cols if ele])
            if len(cols) > 15:
                da.setdefault("nid", cols[1].text.strip())
                da.setdefault("eid", cols[2].text.strip())
                da.setdefault("ename", cols[3].span.attrs['title'] if not cols[3].span.attrs['title'] == '' else '')
                da.setdefault("eaddress", cols[4].span.attrs['title'] if not cols[4].span.attrs['title'] == '' else '')
                da.setdefault("holder", cols[7].text.strip())
                da.setdefault("bto", cols[8].text.strip())
                ttmoney = self.getMoney(cols[2].text.strip(), startTime, endTime)
                da.setdefault("ttimes", ttmoney[0])
                da.setdefault("tmoney", ttmoney[1])
                da.setdefault("stock", cols[11].text.strip())
                da.setdefault("status", cols[12].text.strip())
                data.append(da)
        return data

    def getAllDataByPar(self, **kwargs):
        """
        按照参数获取到彩票机的所有数据
        :parameter devicesId:设备id
        :parameter equipmentName:设备名称
        :parameter startTime:开始时间,类型为字符串yyyy-mm-dd格式
        :parameter endTime:结束时间,类型为字符串yyyy-mm-dd格式
        :parameter id:设备序号
        :parameter network:在线状态
        :parameter goodsState:机头状态
        :parameter isOff:运行状态
        :parameter holderId:商户选择
        :parameter dealerId:经销商选择
        :parameter __hash__ :input.hash值
        :return 返回一个list类型数据:[{'nid': '975',...}]
        """
        f = furl.furl('http://www.kadawo.com/fulei/index.php/equipment/shjList')
        f.args = kwargs
        print(self.getHtml())
        f.args.setdefault('__hash__', SpiderIndex.fltool.getHash(self.getHtml()))
        url = SpiderIndex.fltool.urlReplace(f.url)
        startTime = self.fltool.timeToTimestamp(kwargs['startTime'])
        endTime = self.fltool.timeToTimestamp(kwargs['endTime'])
        print("正在爬取第1页...")
        htm = self.getHtml(url)
        data = self.getIndexData(htm, startTime, endTime)
        totalPage = int(self.getTotalPage(htm))
        i = 2
        while True:
            if i <= totalPage:
                print("正在爬取第%d页，还剩%d页..." % (i, totalPage - i))
                next_url = url + '/p/' + str(i) + '/'
                htm = self.getHtml(next_url)
                d = self.getIndexData(htm, startTime, endTime)  # error!!! ChunkedEncodingError
                data.append(d)
                # time.sleep(1)  # 休眠一秒否则太快会被禁止访问
                i = i + 1
            else:
                break
        return data
        # f = furl.furl('http://www.kadawo.com/fulei/index.php/equipment/shjList')
        # f.args = kwargs
        # f.args.setdefault('__hash__', SpiderIndex.fltool.getHash(self.getHtml()))
        # url = SpiderIndex.fltool.urlReplace(f.url)
        # htm = self.getHtml(url)
        # soup = BeautifulSoup(htm, "lxml")
        # data = self.getIndexData(soup, self.fltool.timeToTimestamp(kwargs['startTime']),
        #                          self.fltool.timeToTimestamp(kwargs['endTime']))
        # return data

    def getAllHolderOrDealer(self, HolderFlag=True):
        """
        得到所有商户或者经销商,默认为商户
        :param HolderFlag: 是否是商户,默认为商户
        :return: 返回一个dict类型集合，key为商户或者经销商id，value为商户或者经销商名称
        {'2': '2-富雷科技-北京富雷科技股份有限公司',...}
        """
        # 这里只获取彩票机首页的html信息
        htm = self.getHtml()
        soup = BeautifulSoup(htm, "lxml")
        if HolderFlag:
            select = soup.find(id='holderId')
        else:
            select = soup.find(id='dealerId')
        option = select.findAll("option")
        data = {}
        for o in option:
            if HolderFlag:
                if not o.text == '商户选择':
                    data.setdefault(o.attrs['value'], o.text)
            else:
                if not o.text == '经销商选择':
                    data.setdefault(o.attrs['value'], o.text)
        return data

    @staticmethod
    def getMoney(eid, startTime, endTime):
        """
        :param eid: 设备id
        :param startTime: 开始时间，时间戳格式
        :param endTime: 结束时间，时间戳格式
        :return: 服务器会返回[次数，金额]
        """
        url = "http://www.kadawo.com/fulei/index.php/equipment/hjslAjax"
        header = FuleiHeader.FuleiHeader.postHjsl()
        login = LoginFulei.LoginFulei()
        header.setdefault('Cookie', 'PHPSESSID=%s' % login.getCookie())
        post_data = "did=" + eid + "&startTime=" + str(startTime) + "&endTime=" + str(endTime)
        result = LoginFulei.LoginFulei.session.post(url, data=post_data, headers=header)
        return result.text.strip('[]').split(',')

    @staticmethod
    def getAllMoney(startTime, endTime, holderId=None, dealerId=None):
        """
        得到某个时间段所有机器的合计金额，合计次数
        :param startTime:开始时间
        :param endTime:结束时间
        :param holderId:商户id
        :param dealerId:经销商id
        :return: 返回一个list,list[0]:合计次数,list[1]:合计金额
        """
        url = "http://www.kadawo.com/fulei/index.php/equipment/zslhj"
        header = SpiderIndex.flheader.postHjsl()
        login = SpiderIndex.login
        header.setdefault('Cookie', 'PHPSESSID=%s' % login.getCookie())
        did = SpiderIndex.getAllIdByUser(holderId=holderId, dealerId=dealerId)
        data = {
            'did': did,
            'startTime': startTime,
            'endTime': endTime,
        }
        result = SpiderIndex.session.post(url, data=data, headers=header)
        return result.text.strip('[]').split(',')

    @staticmethod
    def getAllIdByUser(**kwargs):
        """
        得到某个账户下所有的机器id
        :param kwargs: ["holderId","商户id"] ["dealerId","经销商id"]
        :return: 返回一个字符串:"15位数id,15位数id,..."
        """
        # kwargs只能是一个参数,holderId或者dealerId,否则默认获取dealerId
        url = None
        spider = SpiderIndex()
        if not kwargs == {}:
            if 'holderId' in kwargs.keys() and 'dealerId' in kwargs.keys():
                kwargs = kwargs['dealerId']
            f = furl.furl('http://www.kadawo.com/fulei/index.php/equipment/shjList')
            f.args = kwargs
            f.args.setdefault('__hash__', SpiderIndex.fltool.getHash(spider.getHtml()))
            url = SpiderIndex.fltool.urlReplace(f.url)
        htm = spider.getHtml(url=url)
        pattern = re.compile(r'did:"([0-9]{15}.*)')
        res = re.findall(pattern, htm)
        return res[0].rstrip('",')

# if __name__ == '__main__':
#     spiner = SpiderIndex()
# #     fltool = FuleiTool.FuleiTool()
# #     data = spiner.getAllHolderOrDealer(False)
# #     data = spiner.getTotalPage(spiner.getHtml())
#     data = spiner.getAllDataByPar(startTime='2018-3-1', endTime='2018-4-26')
# #     data = spiner.getAllMoney(str(fltool.getStartTimeOfToday()),str(fltool.getEndTimeOfToday()),dealerId='2')
#     print(data)
