#coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误
from replies.models import Ip,Url

from django.core.servers.basehttp import FileWrapper
import mimetypes
from luntan import settings
import os

from django.http import StreamingHttpResponse

class UploadIpFileForm(forms.Form):
    input_ip_file = forms.FileField()

def display_input_ip(request):
    return render_to_response('input_ip.html')

def handle_file(f,login_name):
    path = 'E:\\Python\\UC\\django\\luntan\\proxy_file\\' + str(login_name) + '_ip.txt'
    # with open(path,'w') as destination:
    destination = open(path,'w')
    lines = f.readlines()
    for line in f.chunks():
        line = line.strip()
        destination.write(line)
    return lines


@csrf_exempt   #处理Post请求出错的情况
def input_ip(request):
    message = []
    login_name = request.session['login_name']
    # Urls = Url.objects.filter(login_name=login_name)
    # Ips = Ip.objects.filter(login_name=login_name)
    # message.append(Urls)
    # message.append(Ips)
    try:
        queryDict = request.POST
        myDict = dict(queryDict.iterlists())   #将queryDict转换成普通的字典
        form = UploadIpFileForm(request.POST,request.FILES)
        if form.is_valid():
            lines = handle_file(request.FILES['input_ip_file'],login_name)
            for line in lines:
                line = line.strip()
                proxies = line.split('\t')
                flag = 1
                try:
                    ip = proxies[0]
                    port = proxies[1]
                    try:
                        ips = Ip.objects.filter(login_name=login_name,ip=ip)      #获取所有的ip相同的元素
                        for iip in ips:
                            print 'iip.ip,iip.port is', iip.ip,iip.port
                            if iip.port == port:            #分别判断这些端口是否已经存在，如果有存在的
                                flag = 0                       #标志位至0，禁止插入数据
                    except:
                        flg = 1
                    print "flag is ",flag
                    if flag:
                        i = Ip(ip=ip,port=port,login_name=login_name)
                        i.save()
                    # print ip,port
                except:
                    print "文件格式有误"
            message.append('导入完成')
        else:
            message.append('导入失败')
        error = False
    except:
        error = True
    return HttpResponse(message)
    # return render_to_response('auto_visit.html',{'message':message})

def output_ip(request):
    print "output_ip"
    file_name = 'E:\\Python\\UC\\django\\luntan\\proxy_file\\root_ip.txt'
    with open(file_name) as f:
        c = f.read()
    return HttpResponse(c)

def file_download(request, filename):

    login_name = request.session['login_name']
    Ips = Ip.objects.filter(login_name=login_name)
    file_path = 'E:\\Python\\UC\\django\\luntan\\luntan\\static\\' + str(login_name) + '_all_ip.txt'   #将所有的ip写入自己的文件
    print "file_path",file_path
    file = open(file_path,'w')
    for proxies in Ips:
        print proxies.ip,proxies.port
        file.write(proxies.ip)
        file.write('\t')
        file.write(proxies.port)
        file.write('\n')

    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    print (filepath)
    wrapper = FileWrapper(open(filepath, 'rb'))
    content_type = mimetypes.guess_type(filepath)[0]
    response = HttpResponse(wrapper, mimetype='content_type')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

@csrf_exempt   #处理Post请求出错的情况
def delete_ip(request):
    message = []
    login_name = request.session['login_name']
    file_name = login_name + '_all_ip.txt'
    Urls = Url.objects.filter(login_name=login_name)
    Ips = Ip.objects.filter(login_name=login_name)
    message.append(Urls)
    message.append(Ips)
    try:
        ip_id = request.POST['id']
        Ip.objects.filter(id = ip_id).delete()
        error = 0
    except:
        error = 1
    return render_to_response('auto_visit.html',{'message':message,'file_name':file_name})
