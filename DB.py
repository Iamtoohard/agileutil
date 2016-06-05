#coding=utf-8

import MySQLdb
import threading

class ThreadLock(object):
    __threadLock  = threading.Lock()

    @staticmethod
    def lock():
        ThreadLock.__threadLock.acquire()

    @staticmethod
    def unlock():
        ThreadLock.__threadLock.release()

class DB(object):

    def __init__(self, host, port, user, passwd, dbName, ispersist=False, log=None, is_mutex = False):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__dbName = dbName
        self.__conn = None
        self.__cur = None
        self.__ispersist = ispersist
        self.__log = log
        self.__is_mutex = is_mutex
        
        if (self.__ispersist):
            DB.connect(self)
            
    def log_error(self, err_info):
        if (self.__log):
            self.__log.error(err_info)

    def connect(self):
        try:
            self.__conn = MySQLdb.connect(
                host = self.__host,
                port = self.__port,
                user = self.__user,
                passwd = self.__passwd,
                db = self.__dbName,
                charset="utf8"
            ) 
            self.__cur = self.__conn.cursor()
        except Exception, ex:
            self.log_error('db connect exception: ' + str(ex))    
            raise ex
    
    def close(self):
        try:
            self.__cur.close()
            self.__conn.close()
        except Exception, ex:
            self.log_error('db close exception: ' + str(ex))    
            raise ex
        
    def lock(self):
        if self.__is_mutex:
            ThreadLock.lock()

    def unlock(self):
        if self.__is_mutex:
            ThreadLock.unlock()

    def update(self, sql):
        self.lock()    
        
        if (not self.__ispersist):
            try:
                self.connect()
            except Exception, ex:
                self.unlock()
                raise ex
        else:
            try:
                self.__conn.ping(True)
            except Exception, ex:
                self.log_error(str(ex))
                try:
                    self.connect()
                except Exception, ex:
                    self.unlock()
                    raise ex

        effect_rows = 0
        try:
            effect_rows = self.__cur.execute(sql)
            self.__conn.commit()
        except Exception, ex:
            self.unlock()
            self.log_error('db update exception: ' + str(ex))    
            raise ex

        if (not self.__ispersist):
            try:
                self.close()
            except Exception, ex:
                self.unlock()
                raise ex
        
        self.unlock()
        return effect_rows

    def query(self, sql):
        self.lock()

        if (not self.__ispersist):
            try:
                self.connect()
            except Exception, ex:
                self.unlock()
                raise ex
        else:
            try:
                self.__conn.ping(True)
            except Exception, ex:
                self.log_error(str(ex))
                try:
                    self.connect()
                except Exception, ex:
                    self.unlock()
                    raise ex

        result = None
        try:
            rows = self.__cur.execute(sql)
            result = self.__cur.fetchmany(rows)
            self.__conn.commit()
        except Exception, ex:
            self.unlock()
            self.log_error('db query exception: ' + str(ex))
            raise ex

        if (not self.__ispersist):
            try:
                self.close()
            except Exception, ex:
                self.unlock()
                raise ex

        self.unlock()
        return result
		
class DBCluster(object):
    def __init__(self, masterDb, slaveDbList = []):
        self._masterDb = masterDb
        self._slaveDbList = slaveDbList
        self._slaveDbCount = len(slaveDbList)
        self._curSlave = 0

    def query(self, sql):
        if len(self._slaveDbList) == 0:
            return self._masterDb.query(sql)
        self._curSlave = self._curSlave + 1
        slaveIndex = self._curSlave % self._slaveDbCount
        slaveDb = self._slaveDbList[slaveIndex]
        return slaveDb.query(sql)

    def queryInstance(self):
        self._curSlave = self._curSlave + 1
        slaveIndex = self._curSlave % self._slaveDbCount
        return slaveIndex

    def update(self, sql):
        return self._masterDb.update(sql)