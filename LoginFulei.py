#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import os
from FuleiHeader import *

__Author__ = '汪思源'
__Vision__ = 0.1
__Date__ = '2018.4.23'

class LoginFulei(object):
    _url = r"http://www.kadawo.com/fulei/index.php/common/doLogin/company/"
    _loginUrl = r"http://www.kadawo.com/fulei/index.php/common/login/company/"
    _indexUrl = r"http://www.kadawo.com/fulei/index.php/index/index"
    session = requests.Session()

    '''
    得到input中的hash值，然后与用户名密码一起提交
    GET http://www.kadawo.com/fulei/index.php/common/login/company HTTP/1.1
    '''
    def getHash(self):
        header = FuleiHeader.getLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        response = LoginFulei.session.get(url=self._loginUrl, headers=header)
        html = response.text
        get_hash_pattern = re.compile(r'<input type="hidden" name="__hash__" value="(.*?)"')
        _hash = re.findall(get_hash_pattern, html)[0]
        return _hash
        # soup = BeautifulSoup(res.text, "html.parser")
        # content = soup.findAll(attrs={"name": "__hash__"})
        # strContent = str(content)
        # getData = re.search(r'value="[0-9a-zA-Z]{32}"', strContent).group()
        # return getData[7:39]

    def getCookie(self):
        if not os.path.exists(r"/fuleiCookie.txt"):
            r = LoginFulei.session.get(url="http://www.kadawo.com/",
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/66.0.3359.117 Safari/537.36'})
            phpsessid = r.cookies['PHPSESSID']
            # 保存Cookie到文件
            self.saveCookie(phpsessid)
        else:
            try:
                f = open(r"/fuleiCookie.txt", 'r')
                phpsessid = f.read()
            finally:
                if f:
                    f.close()
        return phpsessid

    def saveCookie(self,fuleiCookie):
        f = open(r"/fuleiCookie.txt",'w')
        f.write(fuleiCookie)
        f.close()

    '''
    POST http://www.kadawo.com/fulei/index.php/common/doLogin/company/ HTTP/1.1
    '''
    def doLogin(self):
        username = 'fulei'
        password = 'bdxl88888*'
        postUrl = "userName="+username+"&password="+password+"&verify="+"&__hash__="+self.getHash()
        header = FuleiHeader.postDoLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        result = LoginFulei.session.post(self._url,data=postUrl,headers=header)

        # header2 = FuleiHeader.getIndex()
        # header2.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        # req = LoginFulei.session.get(url=self._indexUrl, headers=header2,
        #                     allow_redirects=False)
        # print(req.text)

    '''
    POST http://www.kadawo.com/fulei/index.php/common/checkIsLoginAjax HTTP/1.1
    '''
    def isLogin(self):
        url = "http://www.kadawo.com/fulei/index.php/common/checkIsLoginAjax"
        header = FuleiHeader.postCheckLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        login_code = LoginFulei.session.post(url, data="userId=2",headers=header).content
        if login_code == b'Y':
            return True

        else:
            return False

# if __name__ == '__main__':
#     fulei = LoginFulei()
#     if fulei.isLogin():
#             print('您已经登录')
#     else:
#         fulei.doLogin()