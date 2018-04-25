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

class SpiderIndex(object):
    # 唯一会话id
    login = LoginFulei.LoginFulei()
    flheader = FuleiHeader.FuleiHeader()
    fltool = FuleiTool.FuleiTool()
    session = login.session
    soup = None
    htm = None

    def __init__(self):
        global htm,soup
        htm = self.getHtml()
        # 因为只是获取数据，不是修改，可以用一个BeautifulSoup实例
        soup = BeautifulSoup(htm, "lxml")
        if not SpiderIndex.login.isLogin():
            SpiderIndex.login.doLogin()

    def getHtml(self):
        header = SpiderIndex.flheader.getshjList()
        header.setdefault('Cookie','PHPSESSID=%s' % SpiderIndex.login.getCookie())
        htm = self.session.get(r"http://www.kadawo.com/fulei/index.php/equipment/shjList",headers = header,allow_redirects=False)
        return htm.text

    def writeContent(self):
        global soup
        table = soup.find("table")
        with open(r"/fuleiContent.txt", 'ab') as f:
            for tr in table.findAll('tr'):
                for th in tr.findAll('th'):
                    with open(r"/fuleiContent.txt", 'ab') as fth:
                        fth.write(th.getText().encode('utf-8'))
                        fth.write("\n".encode('utf-8'))
                for td in tr.findAll('td'):
                    with open(r"/fuleiContent.txt", 'ab') as ftd:
                        ftd.write(td.getText().encode('utf-8'))
                        ftd.write("\n".encode('utf-8'))

    def getNextPage(self):
        next_page_pattern = re.compile(r"<a href='(.*?)'>下一页</a>")
        next_page_tag = re.findall(next_page_pattern,self.getHtml())
        next_url = "http://www.kadawo.com%s" % next_page_tag[0]
        return next_url

    '''
     得到首页数据
     序号(nid)2 设备ID(eid)3 设备名称(ename)4 设备地址(eaddress)5 持有人(holder)8
     所属(bto)9 合计次数(ttimes) 合计金额(tmoney) 库存(stock)12 运行状态(status)13
    @return d = [{'nid':'01','eid':'868201049..',...},{....}]
    '''
    def getIndexData(self):
        global soup
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
                ttmoney = SpiderIndex.fltool.getMoney(cols[2].text.strip(),'1524585600','1524671999')#注意数值代表4月25日
                da.setdefault("ttimes",ttmoney[0])
                da.setdefault("tmoney",ttmoney[1])
                da.setdefault("stock",cols[11].text.strip())
                da.setdefault("status",cols[12].text.strip())
                print(da)
                data.append(da)
        print(data)

if __name__ == '__main__':
    spiner = SpiderIndex()
    # spiner.getHtml()
    spiner.getIndexData()
