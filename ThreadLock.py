#coding=utf-8

import threading

class ThreadLock(object):
    """
    互斥锁
    """

    __threadLock  = threading.Lock()

    @staticmethod
    def lock():
        ThreadLock.__threadLock.acquire()

    @staticmethod
    def unlock():
        ThreadLock.__threadLock.release()
