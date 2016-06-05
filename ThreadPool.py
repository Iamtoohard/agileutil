#coding=utf-8

import threading

class MyThread(threading.Thread):
    
    def __init__(self, target, parameter):
        threading.Thread.__init__(self)
        self.__stopFlag = False
        self.__target = target
        self.__parameter = parameter

    def resume(self):
        self.__stopFlag = False

    def stop(self):
        self.__stopFlag = True

    def run(self):
        while (not self.__stopFlag):
            self.__target(self.__parameter)
        
def defaultTarget(threadParameter):
    while True:        
        pass

class ThreadPool(object):

    def __init__(self, threadNum, target, parameter = []):
        self.__threadNum = threadNum
        self.__threadList = []
        self.__target = target
        self.__parameter = parameter

    def getTarget(self):
        return self.__target
        
    def getThreadParameter(self):
        return self.__parameter

    def run(self):
        for item in xrange(self.__threadNum):
            th = MyThread(self.__target, self.__parameter)
            self.__threadList.append(th)
            th.start()

    def stop(self):
        for th in self.__threadList: th.stop()

    def resume(self):
        for th in self.__threadList: th.resume()

    def getThreadNum(self):
        return self.__threadNum