#coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from replies.views import login,search,login_uc,reply,disply_add_url,add_url,add_reply,disply_add_reply,test
from replies.views import delete_url,auto_reply,login_out,delete_content,display_auto_reply
from replies.register_view import display_register,register,display_update_cookie,update_cookie
from replies.auto_visit import display_auto_visit,auto_visit
from visit.views import input_ip,display_input_ip,output_ip,delete_ip
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'luntan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login),            #用户登录

    url(r'^login_out/$', login_out),            #用户退出

    url(r'^login/register.html/$', display_register),                    #展示用户注册界面
    url(r'register.html/$', display_register),            #用户退出后再次展示注册,注意没加^符号，所有以register.html结尾的都会匹配到
    url(r'update_cookie.html/$', display_update_cookie),            #更新cookie,注意没加^符号，所有以register.html结尾的都会匹配到

    url(r'^register/$', register),                                  #调用用户注册逻辑实现函数
    url(r'^update_cookie/$', update_cookie),                                  #调用更新cookie逻辑实现函数


    url(r'^search/$', search),                                      #检查用户名、密码实现登陆
    url(r'^reply/$', reply),                                        #回帖
    url(r'^search/disply_add_url.html/$', disply_add_url),          #展示添加链接界面
    url(r'^reply/disply_add_url.html/$', disply_add_url),           #展示添加链接界面
    url(r'^add_url/$', add_url),                                    #添加url
    url(r'^search/disply_add_reply.html/$', disply_add_reply),      #展示添加回复内容界面
    url(r'^reply/disply_add_reply.html/$', disply_add_reply),      #展示添加回复内容界面
    url(r'^add_reply/$', add_reply),                                #添加回复内容

    url(r'^delete_url/$', delete_url),                          #删除url记录根据id
    url(r'^delete_content/$', delete_content),                  #删除url记录根据


    url(r'^display_auto_reply/$', display_auto_reply),          #展示自动回帖界面
    url(r'^auto_reply/$', auto_reply),                          #自动回帖


    url(r'^display_auto_visit/$', display_auto_visit),          #展示自动访问界面
    url(r'^auto_visit/$', auto_visit),                          #自动访问



    url(r'^input_ip/$', input_ip),
    url(r'input_ip.html/$', display_input_ip),            #导入IP,注意没加^符号，所有以register.html结尾的都会匹配到
    url(r'^output_ip/$', output_ip),
    url(r'^delete_ip/$', delete_ip),

    # url(r'^search/test1.html/$', test),                         #测试test
    url('^fileDownload/filename=(?P<filename>.{1,500})/$', 'visit.views.file_download'),#download 导出IP

    # url(r'^site_static/(?P<path>.*)$','django.views.static.serve',{'document_root':'E:\\Python\\UC\\django\\luntan\\img'}),

)
