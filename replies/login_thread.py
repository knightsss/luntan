# encoding: UTF-8
__author__ = 'shifeixiang'
import threading
import time

import simplejson as json
import os
import cookielib
import Cookie
import urllib2
import urllib
import time
from bs4 import BeautifulSoup
import re

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,Context

from replies.models import Login,Url,Reply,Ip
# from postbartask import ThreadControl



from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
###############################driver相关
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import MySQLdb

class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst

class MyThread(threading.Thread):
    _running=True
    behavior=None
    args=None
    second = 30
    url_list = ""
    content = ""
    def run(self):
        self.behavior(self,self.args,self.second,self.url_list,self.content)
    def stop(self):
        self._running=False

class ThreadControl():
    _running=True
    threadMap={}
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(ThreadControl,cls).__new__(cls,*args,**kwargs)
        return cls._inst

    def start(self,account,second,url_list,content):
        if self.threadMap.has_key(account) == False:
            print "starting:",account
            tt = MyThread();
            tt.behavior=test
            tt.args = account
            tt.second = second
            tt.url_list = url_list
            tt.content = content
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

def test(c_thread,args,second,url_list,content):
    cookie_name = args
    opener = login_jiuyou(cookie_name)
    while c_thread._running:
        for url in url_list:
            posttime,fid,tid,extra,formhash = get_data_from_html(opener,url)          #获取当前页面的参数
            send_content(opener,posttime,fid,tid,extra,formhash,url,content)          #发送数据
            print "hello:",c_thread._running,cookie_name,second,url,content
            time.sleep(3)
        time.sleep(second)
    print "run over!"


def login_jiuyou(cookie_name):
    cookiejar = cookielib.MozillaCookieJar()
    file_path = "E:\\Python\\UC\\django\\luntan\\cookie_file\\" + cookie_name + ".txt"
    print file_path
    f = file(file_path)
    source = f.read()
    targets = json.JSONDecoder().decode(source)
    # print target
    for target in targets:
        cookielib.Cookie
        cookie_item = cookielib.Cookie(
            version=0, name=target['name'],value=target['value'],
                        port=None, port_specified=None,
                        domain=target['domain'], domain_specified=None, domain_initial_dot=None,
                        path=target['path'], path_specified=None,
                        secure=None,
                        expires=None,
                        discard=None,
                        comment=None,
                        comment_url=None,
                        rest=None,
                        rfc2109=False,
            )
        cookiejar.set_cookie(cookie_item)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    return opener

def send_content(opener,posttime,fid,tid,extra,formhash,url,content):
    post_data = urllib.urlencode({
            'mod': 'post',
            'action': 'reply',
            'fid': fid,
            'tid': tid,
            'extra': extra,
            'replysubmit': 'yes',
            'infloat': 'yes',
            'handlekey': 'fastpost',
            'inajax': 1,
            'message': content,
            'posttime': posttime,
            'formhash': formhash,
            'usesig': 1,
        })

    request = urllib2.Request(url)  ##变量
    request.add_header("Cache-Control", "max-age=0")
    request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    request.add_header("Accept-Encoding", "gzip, deflate")
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36")
    # request.add_header("Content-Length", "92")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    request.add_header("Referer", url)###变量
    request.add_header("Origin", "http://bbs.9game.cn")
    # request.add_header("Upgrade-Insecure-Requests", "1")
    request.add_header("Connection", "keep-alive")
    request.add_header("Host", "bbs.9game.cn")

    opener.open(request, post_data)
    print "Reply OK !"

def get_data_from_html(opener,url):
    html = opener.open(url).read()
    # print html
    soup = BeautifulSoup(html)
    ##################get  formhash
    dict = {}
    try:
        formhashs = soup.find(class_='prasie-may').attrs['href']     #存在问题，如果没有任何人回复，则没有prasie-may这个值
    except:
        formhash_all = soup.find_all(class_= re.compile('last'))
        formhashs = formhash_all[1].attrs['href']

    formhash_list = str(formhashs).split('&')
    for formhash in formhash_list:
        child_formhash = formhash.split('=')     #获取key,value
        dict[child_formhash[0]] = child_formhash[1]
    formhash = dict['formhash']
    ###########################get posttimeand fid
    posttime = soup.find(id='posttime').attrs['value']     #获取该元素
    fid = soup.find(class_='curtype').attrs['fid']      #class是python关键字，加下划线处理.attrs['value']

    ##########################get tid and extra
    dict = {}
    try:
        tids = soup.find(class_='cmmnt').attrs['href']
    except:
        tid_all = soup.find_all(class_='authi')
        tids = tid_all[1].find('a').attrs['href']
    tid_list = str(tids).split('&')     #字符串切分
    for tid in tid_list:
        child_tids = tid.split('=')     #获取key,value
        dict[child_tids[0]] = child_tids[1]
    tid = dict['tid']
    extra = "page=" + dict['page']
    return posttime,fid,tid,extra,formhash