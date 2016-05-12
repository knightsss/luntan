#coding=utf-8
__author__ = 'shifeixiang'

from replies.models import Login
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt    #用于处理post请求出现的错误

class UploadFileForm(forms.Form):
    login_name = forms.CharField(max_length=50 )
    pwd = forms.CharField()
    # pwd2 = forms.CharField()
    file = forms.FileField()

class UpdateUploadFileForm(forms.Form):
    file = forms.FileField()

def display_register(request):
    return render_to_response('register.html')

#将上传的文件保存在本地
def handle_file(f,login_name):
    path = 'E:\\Python\\UC\\django\\luntan\\cookie_file\\' + str(login_name) + '.txt'
    with open(path,'w') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@csrf_exempt   #处理Post请求出错的情况
def register(request):
    if request.method == 'POST':
        name = request.POST['login_name']
        pwd = request.POST['pwd']
        file_name = request.FILES['file'].name[:-4]   #获取上传文件的名字
        name_differ = False
        user_exist = False
        try:
            logined_name = Login.objects.get(login_name=name).login_name
            user_exist = True
            return render_to_response('register.html',{'user_exist':user_exist,'name_differ':name_differ})
        except Login.DoesNotExist:
            if file_name == name:
                queryDict = request.POST
                myDict = dict(queryDict.iterlists())   #将queryDict转换成普通的字典
                form = UploadFileForm(request.POST,request.FILES)
                if form.is_valid():
                    try:
                        login = Login(user_name=name,login_name=name,pwd=pwd,power_id=1)
                        login.save()
                        handle_file(request.FILES['file'],name)
                        message = "注册完成！"
                        print "register sucess!"
                    except:
                        print "register faild!"
                    return HttpResponse(message)
                else:
                    message = "注册失败！"
                    return HttpResponse(message)
            else:
                name_differ = True
                return render_to_response('register.html',{'user_exist':user_exist,'name_differ':name_differ,'name':name})
        else:
            message = "用户名不可用！"
            return HttpResponse(message)
    else:
        form = UploadFileForm()
    return render_to_response('register.html')

def display_update_cookie(request):
    return render_to_response('update_cookie.html')

@csrf_exempt   #处理Post请求出错的情况
def update_cookie(request):
    login_name = request.session['login_name']
    file_name = request.FILES['file'].name[:-4]   #获取上传文件的名字
    name_differ = False
    if login_name == file_name:
        queryDict = request.POST
        myDict = dict(queryDict.iterlists())   #将queryDict转换成普通的字典
        form = UpdateUploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_file(request.FILES['file'],login_name)
            message = "更新完成！"
            return HttpResponse(message)
        else:
            message = "更新失败！请检查文件内容是否正确"
            return HttpResponse(message)
    else:
        name_differ = True
        return render_to_response('update_cookie.html',{'name_differ':name_differ})