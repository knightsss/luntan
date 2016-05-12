#coding=utf-8
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
from login_thread import ThreadControl


from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
###############################driver相关
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import MySQLdb
from bs4 import BeautifulSoup
# from PIL import Image
# import pytesseract

# Create your views here.
def login(request):
    # return render_to_response('login.html')
    return render_to_response('login.html')

def login_out(request):
    # return render_to_response('login.html')
    try:
        del request.session['login_name']
    except:
        pass
    return render_to_response('login.html')

####################查询密码和帐号是否一致#########################
@csrf_exempt   #处理Post请求出错的情况
def search(request):
    error = False
    if 'login_name' in request.GET:
        name = request.GET['login_name']
        password = request.GET['pwd']
        if (not name) or (not password):
            error = True
        else:
            # logins = Login.objects.filter(login_name__icontains=name)     #查询时使用filter
            try:
                login = Login.objects.get(login_name=name)
            except:
                error3 = True
                return render_to_response('login.html',{"error3":error3})
            pwd = login.pwd
            if pwd == request.GET['pwd']:           #登陆成功
                # return render_to_response('search_result.html',{'login':login,'query':name})  #测试 密码和账户名一致
                request.session['login_name'] = name
                # return HttpResponse(request.session['login_name'])
                Urls = Url.objects.filter(login_name=name)
                Replys = Reply.objects.filter(login_name=name)
                message = []
                message.append(Urls)
                message.append(Replys)
                return render_to_response('reply.html',{'message':message})
            else:
                error2 = True
                return render_to_response('login.html',{"error2":error2})      #密码胡账户名错误
    return render_to_response('login.html',{"error":error})     #为空时的界面
    # return render_to_response('reply.html',{'message':message})
#添加
def disply_add_url(request):
    return render_to_response('disply_add_url.html')

def add_url(request):
    message = False
    error = False
    try:
        new_url = request.GET['url']
        new_remark = request.GET['remark']
        login_name = request.session['login_name']
        if (not new_url) or (not new_remark):
            error = True
            return render_to_response('disply_add_url.html',{'error':error})
        # message.append(new_url)
        # message.append(new_remark)
        u = Url(url=new_url, remark=new_remark,login_name=login_name,sign='1')           #将数据添加到模板中
        u.save()                      #同步到数据库
        message = True
    except:
        message = False
    return render_to_response('disply_add_url.html',{'message':message})


def disply_add_reply(request):
    return render_to_response('disply_add_reply.html')
    # return render_to_response('test1.html')
def add_reply(request):
    message = False
    error = False
    try:
        new_content = request.GET['content']
        login_name = request.session['login_name']
        if not new_content:
            error = True
            return render_to_response('disply_add_reply.html',{'error':error})
        # message.append(new_content)
        r = Reply(content=new_content,login_name=login_name,sign='1')           #将数据添加到模板中,修改
        r.save()                      #同步到数据库
        # message.append('sucess')
        message = True
    except:
        message = False
    return render_to_response('disply_add_reply.html',{'message':message})


def test(request):
    return render_to_response('test1.html')
#回复
@csrf_exempt   #处理Post请求出错的情况
def reply(request):
    message = []
    login_name = request.session['login_name']
    Urls = Url.objects.filter(login_name=login_name)
    Replys = Reply.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Replys)
    try:
        cookie_name = request.session['login_name']
        print cookie_name
        opener = login_jiuyou(cookie_name)
        try:
            elements = request.POST #request.getParameterValues('url_radio')\    #获取所有参数
            url_list = elements.lists()[0][1]                   #过滤后剩余urls列表相关参数
            content = request.POST['reply_radio']
        except:
            print "error"
            error = True
            return render_to_response('reply.html',{'message':message})         #如果从自动回帖返回或者其他地方进来，则content会获取失败，进而不会显示发送失败还是成功，只显示数据页面。

        content = content.encode('utf-8')
        for url in url_list:
            print url,"开始回帖..."
            posttime,fid,tid,extra,formhash = get_data_from_html(opener,url)          #获取当前页面的参数
            send_content(opener,posttime,fid,tid,extra,formhash,url,content)          #发送数据
        message.append(1)
        flag=True
    except:
        flag=False
        message.append(0)
    # return HttpResponse(request.session['login_name'])
    return render_to_response('reply.html',{'message':message,'flag':flag})


#自动回复
@csrf_exempt   #处理Post请求出错的情况
def auto_reply(request):
    message = []
    author = request.session['login_name']
    print'author is', author
    Urls = Url.objects.filter(login_name=author)
    Replys = Reply.objects.filter(login_name=author)
    message.append(Urls)
    message.append(Replys)
    try:
        second = request.POST['set_time_name']
    except:
        print "end"
        second = 60
    second = int(second)

    s = request.POST['s_radio']
    try:
        elements = request.POST    #获取所有参数
        url_list = elements.lists()[1][1]                   #过滤后剩余urls列表相关参数
        # url = request.POST['url_radio']
        content = request.POST['reply_radio']
        # return HttpResponse(url_list)
    except:
        url = ""
        content = ""
    if s == 'start':
        flag = 1
    if s == 'end':
        flag = 0
    print "s",s
    content = content.encode('utf-8')
    t1 = ThreadControl()
    if s == 'start':
        print "start..."
        t1.start(author,second,url_list,content)
        # message.append(second)
        # request.session['reply']
        message.append(1)
    if s == 'end':
        print "stop..."
        t1.stop(author)
        message.append(0)
    return render_to_response('auto_reply.html',{'message':message})
    # try:
    #     cookie_name = request.session['login_name']
    #     opener = login_jiuyou(cookie_name)
    #     try:
    #         url = request.POST['url_radio']
    #         content = request.POST['reply_radio']
    #
    #     except:
    #         error = True
    #         return render_to_response('auto_reply.html',{'message':message})
    #     # content = "23333333"
    #     content = content.encode('utf-8')
    #     if s == 'start':
    #         t1.start(author,second,url,content)
    #         # message.append(second)
    #         # request.session['reply']
    #         message.append(1)
    #     if s == 'end':
    #         print "start_stop..."
    #         t1.stop(author)
    #         message.append(0)
    #     # count = int(count)
    #     # for num in range(count):
    #     #     time.sleep(int(second))
    #     #     print url
    #     #     # posttime,fid,tid,extra,formhash = get_data_from_html(opener,url)          #获取当前页面的参数
    #     #     # send_content(opener,posttime,fid,tid,extra,formhash,url,content)          #发送数据
    #
    # except:
    #     return HttpResponse("error")
    # return render_to_response('auto_reply.html',{'message':message})


def display_auto_reply(request):
    message = []
    author = request.session['login_name']
    Urls = Url.objects.filter(login_name=author)
    Replys = Reply.objects.filter(login_name=author)
    message.append(Urls)
    message.append(Replys)
    return render_to_response('auto_reply.html',{'message':message})
    # author = request.session['login_name']
    # t = loader.get_template('auto_reply.html')
    # c = Context({
    #     'message':message,
    #     'current_author':author,
    # })
    # return t.render(c)
    # return render_to_response('auto_reply.html',{'message':message})


#删除url记录
@csrf_exempt   #处理Post请求出错的情况
def delete_url(request):
    message = []
    login_name = request.session['login_name']
    Urls = Url.objects.filter(login_name=login_name)
    Replys = Reply.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Replys)
    try:
        url_id = request.POST['id']
        Url.objects.filter(id = url_id).delete()
        error = 0
    except:
        error = 1
    return render_to_response('reply.html',{'message':message})

#删除回复内容记录
@csrf_exempt   #处理Post请求出错的情况
def delete_content(request):
    message = []
    login_name = request.session['login_name']
    Urls = Url.objects.filter(login_name=login_name)
    Replys = Reply.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Replys)
    try:
        content_id = request.POST['id']
        Reply.objects.filter(id = content_id).delete()
        error = 0
    except:
        error = 1
    return render_to_response('reply.html',{'message':message})

def login_jiuyou(cookie_name):
    cookiejar = cookielib.MozillaCookieJar()
    file_path = "E:\\Python\\UC\\django\\luntan\\cookie_file\\" + cookie_name + ".txt"     #更改
    print file_path
    f = file(file_path)
    source = f.read()
    targets = json.JSONDecoder().decode(source)
    # print target
    for target in targets:
        # cookielib.Cookie
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
    try:
        opener.open(request, post_data)
        print "Reply OK !"
    except:
        print "Reply Faild !"

def get_data_from_html(opener,url):
    html = opener.open(url).read()
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

def get_data_from_html_old(opener,url):
    html = opener.open(url).read()
    soup = BeautifulSoup(html)
    # print soup.find(id='posttime')

    # formhash = soup.find(id='scbar_form')
    # print formhash
    dict = {}
    formhashs = soup.find(class_='prasie-may').attrs['href']
    formhash_list = str(formhashs).split('&')
    for formhash in formhash_list:
        child_formhash = formhash.split('=')     #获取key,value
        dict[child_formhash[0]] = child_formhash[1]
    formhash = dict['formhash']

    posttime = soup.find(id='posttime').attrs['value']     #获取该元素
    fid = soup.find(class_='curtype').attrs['fid']      #class是python关键字，加下划线处理.attrs['value']
    tids = soup.find(class_='cmmnt').attrs['href']

    dict = {}
    tid_list = str(tids).split('&')     #字符串切分
    for tid in tid_list:
        child_tids = tid.split('=')     #获取key,value
        dict[child_tids[0]] = child_tids[1]
    tid = dict['tid']
    extra = "page=" + dict['page']
    return posttime,fid,tid,extra,formhash



















############################登陆uc#######################
# def login_uc(request):
#     # request.GET['driver'].
#     return

#######################获取验证码###############################
def get_uc_captcha():
     #----------谷歌浏览器
    chromedriver = "F:\\auto_windows\\atom-windows\\Atom\\chromedriver\\chromedriver.exe"   #谷歌浏览器位置
    os.environ["webdriver.chrome.driver"] = chromedriver            #设置环境变量
    driver = webdriver.Chrome(chromedriver)             #webdriver获取
    #----------火狐浏览器
    # driver = webdriver.Firefox()
    driver.maximize_window()                            #窗口最大化

    driver.get('http://bbs.uc.cn/member.php?mod=logging&action=login&referer=')                   #获取uc登陆首页地址
    time.sleep(3)                                       #延时3秒

    driver.find_element_by_id('login_name').send_keys('1251314160@qq.com')
    driver.find_element_by_id('password').send_keys('sfx918')

    # driver.find_element_by_class_name('refreshCaptcha').click()
    # time.sleep(3)
    # driver.find_element_by_id('captcha_code').click()
    driver.save_screenshot('E:\\Python\\UC\\django\\luntan\\img\\all.png')       #截取当前网页，该网页有我们需要的验证码
    captcha_element = driver.find_element_by_xpath('//*[@id="dCaptcha"]/td/img')    #定位验证码
    location = captcha_element.location         #获取验证码x,y轴坐标
    size=captcha_element.size               #获取验证码的长宽
    rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
    # i=Image.open("E:\\Python\\UC\\django\\luntan\\img\\all.png")             #打开截图
    # frame=i.crop(rangle)                 #使用Image的crop函数，从截图中再次截取我们需要的区域
    # img_path = "E:\\Python\\UC\\django\\luntan\\img\\uc_captcha.jpg"
    # frame.save(img_path)
    # return driver
    # img_path = change_captcha(driver)    #更改图片并存储
        # recognise_code(img_path)

def login_uc(request):
    driver = request.POST['driver']
    # return render_to_response('login_result.html')
    return render_to_response(driver)
#更改图片并存储
# def change_captcha(driver):
#     driver.save_screenshot('E:\\Python\\UC\\django\\luntan\\img\\all.png')       #截取当前网页，该网页有我们需要的验证码
#     captcha_element = driver.find_element_by_xpath('//*[@id="dCaptcha"]/td/img')    #定位验证码
#     location = captcha_element.location         #获取验证码x,y轴坐标
#     size=captcha_element.size               #获取验证码的长宽
#     rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
#     i=Image.open("E:\\Python\\UC\\django\\luntan\\img\\all.png")             #打开截图
#     frame=i.crop(rangle)                 #使用Image的crop函数，从截图中再次截取我们需要的区域
#     img_path = "E:\\Python\\UC\\django\\luntan\\img\\captcha.jpg"
#     frame.save(img_path)
#     return img_path



# @csrf_exempt   #处理Post请求出错的情况
# def auto_reply_deal(request):
#     message = []
#     flag = 0
#     Urls = Url.objects.get_queryset()
#     Replys = Reply.objects.get_queryset()
#     # message.append(Urls)
#     # message.append(Replys)
#     # url = request.POST['url_radio']
#     # content = request.POST['reply_radio']
#     # radio = request.POST['s_radio']
#     # time = request.POST['set_time_name']
#     # message.append(url)
#     # message.append(content)
#     # message.append(radio)
#     # message.append(time)
#     # return HttpResponse(message)
#     try:
#         opener = login_jiuyou()
#
#         # url = "http://bbs.9game.cn/forum.php?mod=viewthread&tid=17834214&extra=page%3D3%26filter%3Dtypeid%26typeid%3D46918%26typeid%3D46918"
#         try:
#             url = request.POST['url_radio']
#             content = request.POST['reply_radio']
#             radio = request.POST['s_radio']
#             time = request.POST['set_time_name']
#             if radio=='start':
#                 flag = 1
#         except:
#             error = True
#             return render_to_response('auto_reply.html',{'message':message})
#         while(flag):
#             content = content.encode('utf-8')
#             # posttime,fid,tid,extra,formhash = get_data_from_html(opener,url)          #获取当前页面的参数
#             # send_content(opener,posttime,fid,tid,extra,formhash,url,content)          #发送数据
#             print "reply_ing"
#
#             time.sleep(time)
#             if radio == 'end':
#                 flag = 0
#             print radio
#         message.append(1)
#     except:
#          message.append(0)
#     return render_to_response('auto_reply_deal.html',{'message':message})