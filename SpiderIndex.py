#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
爬取彩票机首页数据
1.得到Session会话对象
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

    '''
    得到某一页的Html信息
    '''
    def getHtml(self,url = None):
        header = SpiderIndex.flheader.getshjList()
        header.setdefault('Cookie','PHPSESSID=%s' % SpiderIndex.login.getCookie())
        if url:
            htm = self.session.get(url,headers=header,allow_redirects=False)
        else:
            htm = self.session.get(r"http://www.kadawo.com/fulei/index.php/equipment/shjList", headers=header,
                                   allow_redirects=False)
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

    def getNextPage(self,url = None):
        next_page_pattern = re.compile(r"<a href='(.*?)'>下一页</a>")
        next_page_tag = re.findall(next_page_pattern,self.getHtml(url=url))
        next_url = "http://www.kadawo.com%s" % next_page_tag[0]
        return next_url

    '''
     得到某一页的数据
     序号(nid)2 设备ID(eid)3 设备名称(ename)4 设备地址(eaddress)5 持有人(holder)8
     所属(bto)9 合计次数(ttimes) 合计金额(tmoney) 库存(stock)12 运行状态(status)13
    @return d = [{'nid':'01','eid':'868201049..',...},{....}]
    @:parameter startTime => TimeStamp
    @:parameter endTime => TimeStamp
    '''
    def getIndexData(self,soup,startTime = None,endTime = None):
        if not startTime:
            startTime = self.fltool.getStartTimeOfToday()
        if not endTime:
            endTime = self.fltool.getEndTimeOfToday()
        data = []
        tbody = soup.find("tbody")
        rows = tbody.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            da = {}
            # cols = [ele.text.strip() for ele in cols]
            # print(cols)
            # data.append([ele for ele in cols if ele])
            if len(cols) > 15:
                da.setdefault("nid",cols[1].text.strip())
                da.setdefault("eid",cols[2].text.strip())
                da.setdefault("ename",cols[3].span.attrs['title'])
                da.setdefault("eaddress",cols[4].span.attrs['title'])
                da.setdefault("holder",cols[7].text.strip())
                da.setdefault("bto",cols[8].text.strip())
                ttmoney = self.getMoney(cols[2].text.strip(),startTime,endTime)
                da.setdefault("ttimes",ttmoney[0])
                da.setdefault("tmoney",ttmoney[1])
                da.setdefault("stock",cols[11].text.strip())
                da.setdefault("status",cols[12].text.strip())
                data.append(da)
        return data

    '''
    得到所有商户或者经销商,默认为商户
    '''
    def getAllHolderOrDealer(self,HolderFlag = True):
        #这里只获取彩票机首页的html信息
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

    '''
    按照参数获取到彩票机的所有数据
    @parameter devicesId => 设备id
    @parameter equipmentName => 设备名称
    @parameter startTime => 开始时间
    @parameter endTime => 结束时间
    @parameter id => 设备序号
    @parameter network => 在线状态
    @parameter goodsState => 机头状态
    @parameter isOff => 运行状态
    @parameter holderId => 商户选择
    @parameter dealerId => 经销商选择
    @parameter __hash__ => input.hash值
    Time = yyyy-mm-dd
    '''
    def getAllDataByPar(self,**kwargs):
        f = furl.furl('http://www.kadawo.com/fulei/index.php/equipment/shjList')
        f.args = kwargs
        f.args.setdefault('__hash__',SpiderIndex.fltool.getHash(self.getHtml()))
        url = SpiderIndex.fltool.urlReplace(f.url)
        htm = self.getHtml(url)
        soup = BeautifulSoup(htm,"lxml")
        data = self.getIndexData(soup, self.fltool.timeToTimestamp(kwargs['startTime']),
                                 self.fltool.timeToTimestamp(kwargs['endTime']))
        return data

    '''
    得到某个时间段单个机器的合计金额,合计次数
    startTime与endTime是时间戳格式
    服务器会返回[次数，金额]
    '''
    @staticmethod
    def getMoney(eid, startTime, endTime):
        url = "http://www.kadawo.com/fulei/index.php/equipment/hjslAjax"
        header = FuleiHeader.FuleiHeader.postHjsl()
        login = LoginFulei.LoginFulei()
        header.setdefault('Cookie', 'PHPSESSID=%s' % login.getCookie())
        post_data = "did="+eid+"&startTime="+str(startTime)+"&endTime="+str(endTime)
        result = LoginFulei.LoginFulei.session.post(url,data=post_data,headers=header)
        return result.text.strip('[]').split(',')

    '''
    得到某个时间段所有机器的合计金额，合计次数
    与getMoney类似
    '''
    @staticmethod
    def getAllMoney():
        pass

    '''
    得到某个账户下所有的机器id
    :kwargs = ["holderId","商户id"] ["dealerId","经销商id"]
    '''
    def getAllIdByUser(self,**kwargs):
        #kwargs只能是一个参数,holderId或者dealerId,否则默认获取dealerId
        url = None
        if not kwargs == {}:
            f = furl.furl('http://www.kadawo.com/fulei/index.php/equipment/shjList')
            f.args = kwargs
            f.args.setdefault('__hash__',SpiderIndex.fltool.getHash(SpiderIndex.getHtml()))
            url = SpiderIndex.fltool.urlReplace(f.url)
        htm = self.getHtml(url=url)
        soup = BeautifulSoup(htm,'lxml')
        pattern = re.compile(r'did:"([0-9]{15},).*?')
        res = re.findall('did:"[0-9]{15},.*?',htm)
        print(res)
        # script = soup.findAll("script",text=pattern)
        # print(script)
        # print(pattern.search(script.text).group(1))


if __name__ == '__main__':
    spiner = SpiderIndex()
    # data = spiner.getAllHolderOrDealer(False)
    # data = spiner.getNextPage()
    # data = spiner.getAllDataByPar(startTime='2018-3-1',endTime='2018-4-26')
    # print(data)
    spiner.getAllIdByUser()