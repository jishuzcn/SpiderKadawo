#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Request Header TOOL - write by 汪思源
目的：完全模拟浏览器发送请求
'''
class FuleiHeader(object):
    '''
    GET http://www.kadawo.com/fulei/index.php/common/login/company HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def getLogin():
        header = {'Host':'www.kadawo.com',
                  'Proxy-Connection':'keep-alive',
                  'pgrade-Insecure-Requests':'1',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    POST http://www.kadawo.com/fulei/index.php/common/doLogin/company/ HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def postDoLogin():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Content-Length':'84',
                  'Cache-Control':'max-age=0',
                  'Origin':'http://www.kadawo.com',
                  'Upgrade-Insecure-Requests':'1',
                  'Content-Type':'application/x-www-form-urlencoded',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer':'http://www.kadawo.com/fulei/index.php/common/login/company/',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    GET http://www.kadawo.com/fulei/index.php/index/index HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def getIndex():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/common/doLogin/company/',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    POST http://www.kadawo.com/fulei/index.php/common/checkIsLoginAjax HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def postCheckLogin():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Content-Length': '8',
                  'Accept': '*/*',
                  'Origin':'http://www.kadawo.com',
                  'X-Requested-With':'XMLHttpRequest',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/index/index',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    GET http://www.kadawo.com/fulei/index.php/equipment/shjList HTTP/1.1
    缺少Cookie值
    得到彩票机列表
    '''
    @staticmethod
    def getshjList():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/index/amTable',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    POST http://www.kadawo.com/fulei/index.php/equipment/hjslAjax  HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def postHjsl():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'application/json, text/javascript, */*; q=0.01',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/equipment/shjList',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'X-Requested-With':'XMLHttpRequest',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'Origin':'http://www.kadawo.com',
                  }
        return header

    '''
    GET http://www.kadawo.com/fulei/index.php/equipment/shjList/startTime/2018-04-11/endTime/2018-04-25/__hash__/hash/ 
    HTTP/1.1
    缺少Cookie值
    '''
    @staticmethod
    def getShjByDate():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/equipment/shjList',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    '''
    GET http://www.kadawo.com/fulei/index.php/equipment/signIn/did/867793034478521 HTTP/1.1
    '''
    @staticmethod
    def getSingle():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/index/amTable',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'}
        return header

