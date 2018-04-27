#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import FuleiHeader
import FuleiTool

__Author__ = '汪思源'
__Vision__ = 0.1
__Date__ = '2018.4.23'


class LoginFulei(object):
    _url = r"http://www.kadawo.com/fulei/index.php/common/doLogin/company/"
    _loginUrl = r"http://www.kadawo.com/fulei/index.php/common/login/company/"
    _indexUrl = r"http://www.kadawo.com/fulei/index.php/index/index"
    # 得到唯一的对话实例
    session = requests.Session()
    flheader = FuleiHeader.FuleiHeader()
    fltool = FuleiTool.FuleiTool()

    def __init__(self):
        # 如果未登录就删除Cookie，否则带过期的Cookie会导致无法登陆，次数多服务器限制ip
        if not self.isLogin():
            if os.path.exists(r"/fuleiCookie.txt"):
                os.remove(r"/fuleiCookie.txt")

    @staticmethod
    def getCookie():
        if not os.path.exists(r"/fuleiCookie.txt"):
            r = LoginFulei.session.get(url="http://www.kadawo.com/",
                      headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/66.0.3359.117 Safari/537.36'})
            phpsessid = r.cookies['PHPSESSID']
            # 保存Cookie到文件
            LoginFulei.saveCookie(phpsessid)
        else:
            try:
                f = open(r"/fuleiCookie.txt", 'r')
                phpsessid = f.read()
            finally:
                if f:
                    f.close()
        return phpsessid

    @staticmethod
    def saveCookie(fuleiCookie):
        f = open(r"/fuleiCookie.txt",'w')
        f.write(fuleiCookie)
        f.close()

    '''
    POST http://www.kadawo.com/fulei/index.php/common/doLogin/company/ HTTP/1.1
    '''
    def doLogin(self):
        username = 'fulei'
        password = 'bdxl88888*'
        header = LoginFulei.flheader.getLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        response = LoginFulei.session.get(url=self._loginUrl, headers=header)
        _hash = LoginFulei.fltool.getHash(response.text)

        postData = "userName="+username+"&password="+password+"&verify="+"&__hash__="+_hash
        header = LoginFulei.flheader.postDoLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        result = LoginFulei.session.post(self._url,data=postData,headers=header)

    '''
    POST http://www.kadawo.com/fulei/index.php/common/checkIsLoginAjax HTTP/1.1
    '''
    def isLogin(self):
        url = "http://www.kadawo.com/fulei/index.php/common/checkIsLoginAjax"
        header = LoginFulei.flheader.postCheckLogin()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.getCookie())
        login_code = LoginFulei.session.post(url, data="userId=2",headers=header).content
        if login_code == b'Y':
            return True
        else:
            return False
    '''
    1.得到userId
    2.判断权限
    '''
    def check_id(self):
        pass

# if __name__ == '__main__':
#     fulei = LoginFulei()
#     if fulei.isLogin():
#             print('您已经登录')
#     else:
#         fulei.doLogin()