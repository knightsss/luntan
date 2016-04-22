#coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from replies.views import login,login_result,search,login_uc,reply,disply_add_url,add_url,add_reply,disply_add_reply,test
from replies.views import delete_url,auto_reply,login_out,delete_content
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'luntan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login),
    url(r'^login_out/$', login_out),
    # url(r'^login_result/$', login_result),
    url(r'^search/$', search),
    url(r'^reply/$', reply),
    url(r'^search/disply_add_url.html/$', disply_add_url),          #展示添加链接界面
    url(r'^reply/disply_add_url.html/$', disply_add_url),           #展示添加链接界面
    url(r'^add_url/$', add_url),
    url(r'^search/disply_add_reply.html/$', disply_add_reply),      #展示添加回复内容界面
    url(r'^reply/disply_add_reply.html/$', disply_add_reply),      #展示添加回复内容界面
    url(r'^add_reply/$', add_reply),        #添加回复内容

    url(r'^delete_url/$', delete_url),          #删除url记录根据id
    url(r'^delete_content/$', delete_content),          #删除url记录根据

    url(r'^auto_reply/$', auto_reply),          #自动回帖

    url(r'^search/test1.html/$', test),

    url(r'^site_static/(?P<path>.*)$','django.views.static.serve',{'document_root':'E:\\Python\\UC\\django\\luntan\\img'}),

)
