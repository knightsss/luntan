# encoding: UTF-8
'''
Created on 2016年4月21日

@author: yangchaojun
'''
import threading
import time

class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst

class Postbartask(threading.Thread):
    _running=True
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Postbartask,cls).__new__(cls,*args,**kwargs)
        return cls._inst
    def run(self):
        while self._running:
            time.sleep(1)
            print "hello"
        else:
            print "stop"
    def stop(self):
        self._running=False
        
t=Postbartask()
t.start()
time.sleep(5)
t2=Postbartask()
t2.stop()