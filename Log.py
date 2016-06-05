#coding=utf-8

import logging
from logging.handlers import WatchedFileHandler

class Log(object):
    
    __logList = {}
    __fmt = '%(asctime)s-%(filename)s-%(process)d-%(thread)d-%(funcName)s-[line:%(lineno)d]-%(levelname)s-%(message)s'
    #__fmt = '[%(levelname)s] [%(threadName)s] [%(process)d] %(asctime)s [line:%(lineno)d] %(message)s'
    __level = logging. DEBUG

    def __init__(self, path):
        self.__path = path
        self.__isOutput = False
        self.__switch = True
        self.__formatter = logging.Formatter(Log.__fmt)
        self.__fileHandler = WatchedFileHandler(self.__path)
        self.__fileHandler.setFormatter(self.__formatter)
        self.__logger = logging.getLogger(path)
        self.__logger.addHandler(self.__fileHandler)
        self.__outputHandler = None
        self.__logger.setLevel(Log.__level)
        self._errorCallBack = None
        self._warningCallBack = None
        Log.__logList[path] = self
    
    @staticmethod
    def getInstance(path):
        
        for key in Log.__logList.keys():
            if (not cmp(key, path)):
                return Log.__logList[key]
        log = Log(path)
        Log.__logList[path] = log
        return log

    def setSwitch(self, switch):
        
        if not (switch == True or switch == False):
            raise TypeError("parameter's type should be bool")
        self.__switch = switch
        
    def getSwitchStatus(self):
        
        return self.__switch

    def setOutput(self, isOutput):
        
        if (isOutput == self.__isOutput):
            return
        if self.__isOutput:
            if not self.__outputHandler:
                self.__isOutput = isOutput
                return
            else:
                self.__logger.removeHandler(self.__outputHandler) 
        else:
            if not self.__outputHandler:
                self.__outputHandler = logging.StreamHandler()
                self.__outputHandler.setFormatter(self.__formatter)
                self.__logger.addHandler(self.__outputHandler)
                self.__logger.setLevel(Log.__level)
            else:
                self.__logger.addHandler(self.__outputHandler)
                self.__logger.setLevel(Log.__level)

    def getOutputStatus(self):
        
        return self.__isOutput

    def getPath(self):
        
        return self.__path

    def getLogger(self):
        return self.__logger

    def debug(self, loginfo):
        if self.__switch:
            self.__logger.debug(loginfo)

    def info(self,logInfo):
        if self.__switch:
            self.__logger.info(logInfo)

    def warning(self, logInfo):
        if self.__switch:
            self.__logger.warning(logInfo)
        if self._warningCallBack:
            self._warningCallBack(logInfo)

    def error(self, logInfo):
        if self.__switch:
            self.__logger.error(logInfo)
        if self._errorCallBack:
            self._errorCallBack(logInfo)

    def setErrorCallBack(self, func):
        self._errorCallBack = func

    def setWarningCallBack(self, func):
        self._warningCallBack = func

