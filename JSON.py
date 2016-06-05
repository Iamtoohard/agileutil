#coding=utf-8

import json

class JSON(object):
    def __init__(self, json_str = None):
        self.__json_str = json_str
        pass
    
    def set_json_str(self, json_str):
        self.__json_str = json_str
    
    def get_json_str(self):
        return self.__json_str
    
    @staticmethod
    def check_json(json_str):
        ret = True
        try:
            json.loads(json_str)
        except Exception, ex:
            ret = False
        return ret
    
    @staticmethod
    def decode(json_str):
        return json.loads(json_str)
        
    @staticmethod
    def encode(json_data):
        return json.dumps(json_data)
    
    def length(self):
        list_tmp = self.decode(self.__json_str)
        return len(list_tmp)
    
    def get(self, key):
        json_data = JSON.decode(self.__json_str)
        json_data = json_data[key]
        json_str = JSON.encode(json_data)
        new_instance = JSON(json_str)
        return new_instance

    def has_key(self, key):
        json_data = JSON.decode(self.__json_str)
        try:
            json_data = json_data[key]
        except Exception, ex:
            return False
        return True

    def toList(self):
        return list(JSON.decode(self.__json_str))

    def toString(self):
        return str(JSON.decode(self.__json_str))

    def toInt(self):
        return int(self.__json_str)

    def toFloat(self):
        return float(self.__json_str.replace("\"", ""))