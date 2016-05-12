# encoding: UTF-8
__author__ = 'shifeixiang'
import threading
import simplejson as json
import cookielib
import Cookie
import urllib2
import urllib
import time

from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
###############################driver相关
import os
from datetime import datetime
import time

class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst

class MyThread_visit(threading.Thread):
    _running=True
    behavior=None
    args=None
    second = 30
    count = 1000
    url_list = ""
    proxy_list = ""
    # port_list = ""
    def run(self):
        self.behavior(self,self.args,self.second,self.count, self.url_list,self.proxy_list)
    def stop(self):
        self._running=False

class ThreadControl_visit():
    _running=True
    threadMap={}
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(ThreadControl_visit,cls).__new__(cls,*args,**kwargs)
        return cls._inst

    def start(self,account,second,count,url_list,proxy_list):
        if self.threadMap.has_key(account) == False:
            print "starting:",account
            tt = MyThread_visit();
            tt.behavior=visit
            tt.args = account
            tt.second = second
            tt.count = count
            tt.url_list = url_list
            tt.proxy_list = proxy_list
            # tt.port_list = port_list
            tt.start()
            self.threadMap[account]=tt

    def stop(self,account):
        if self.threadMap.has_key(account) == True:
            print "stopping:",account
            tt=self.threadMap[account]
            tt.stop()
            try:
                self.threadMap.pop(account)
            except:
                pass

def visit(c_thread,args,second,count,url_list,proxy_list):
    cookie_name = args
    while c_thread._running:
        for proxy in proxy_list:
            if count < 1:
                c_thread._running = False
                break
            proxy_set = {'http':proxy}
            opener = urllib.FancyURLopener(proxy_set)
            for url in url_list:
                try:
                    f = opener.open(url)
                except:
                    print "error!"
                print datetime.today(),c_thread._running,cookie_name,second,count,url,proxy
                time.sleep(3)
            count = count - 1
            time.sleep(second)

