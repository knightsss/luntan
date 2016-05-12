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

class MyThread(threading.Thread):
    _running=True
    account=""
    def run(self):
        while self._running:
            time.sleep(1)
            print "hello:",self.account
        else:
            print "stop:",self.account
    def stop(self):
        self._running=False

class ThreadControl():
    _running=True
    threadMap={}
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(ThreadControl,cls).__new__(cls,*args,**kwargs)
        return cls._inst
    
    def start(self,account):
        if self.threadMap.has_key(account) == False:
            print "starting:",account
            tt = MyThread();
            tt.start()
            tt.account=account
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
