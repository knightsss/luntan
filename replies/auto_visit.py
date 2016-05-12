#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
import numpy
from replies.models import Url,Reply,Ip
from replies.visit_thread import ThreadControl_visit

def display_auto_visit(request):
    message = []
    login_name = request.session['login_name']
    file_name = login_name + '_all_ip.txt'
    print file_name
    Urls = Url.objects.filter(login_name=login_name)
    Ips = Ip.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Ips)
    # return HttpResponse(message)
    return render_to_response('auto_visit.html',{'message':message,'file_name':file_name})

@csrf_exempt   #处理Post请求出错的情况
def auto_visit(request):
    message = []
    login_name = request.session['login_name']
    Urls = Url.objects.filter(login_name=login_name)
    Ips = Ip.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Ips)
    ip_list = []
    port_list = []
    proxy_list = []
    sign = request.POST['s_radio']              #获取开始或者结束标志
    login_name = request.session['login_name']  #获取登录名
    try:
        second = request.POST['set_time_name']  #获取时间
        count = request.POST['set_count_name']  #获取次数
    except:
        second = 60
        count  = 100
    second = int(second)
    count = int(count)
    if count == 0:
        count = 1000
    element = request.POST
    url_list = element.lists()[1][1]
    Ips = Ip.objects.filter(login_name=login_name).values('ip')     #过滤后获取IP的值
    Posts = Ip.objects.filter(login_name=login_name).values('port') #过滤后获取port的值
    for ip_set in Ips:
        ip_list.append(ip_set['ip'])                        #获取ip列表
    for port_set in Posts:
        port_list.append(port_set['port'])                  #获取port列表
    for i in range(len(ip_list)):
        proxy = 'http://' + ip_list[i] + ':' + port_list[i]
        proxy_list.append(proxy)
    try:
        c = ThreadControl_visit()
        if sign == 'start':
            c.start(login_name,second,count,url_list,proxy_list)
            message.append(1)
        if sign == 'end':
            c.stop(login_name)
            message.append(0)
        # message.append(1)
        error = False
    except:
        error = True
    return render_to_response('auto_visit.html',{'message':message,'error':error})