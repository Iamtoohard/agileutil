#coding=utf-8

import os
import re
import sys
import json
import stat
import time
import hashlib
import urllib
import urllib2
import base64
import logging
import datetime
import threading
import platform
import commands
import logging.handlers
from _codecs import decode
from multiprocessing import Process
#from setproctitle import setproctitle
from logging.handlers import WatchedFileHandler

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return  m.hexdigest()

def set_proc_title(procName):
    try:
        setproctitle(procName)
        return 0
    except:
        return -1

def itoa(ascii_value):
    return chr(ascii_value)

def atoi(char):
    return ord(char)

def get_cur_os():
    return sys.platform

def one_instance(proc_name, sig = None):
    pid_list = get_pid_list(proc_name)
    cur_pid = os.getpid()
    if not sig:
        sig = 34
    kill_num = 0
    for pid in pid_list:
        if pid != cur_pid:
            kill(pid, sig)
            kill_num = kill_num + 1
    return kill_num

def exit(text = None):
    if text:
        print text
    sys.exit()

def findall(regex, text):
    pattern = re.compile(regex)
    search_result = pattern.findall(text)
    return search_result

def get_file_size(filename):
    return os.path.getsize(filename)

def kill(pid, sig):
    os.kill(pid, sig)

def create_standard_daemon():
    if os.fork() > 0:
        sys.exit(0)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    if (os.fork() > 0):
        sys.exit(0)
    return True

def create_simple_daemon():
    if (os.fork() > 0):
        sys.exit(0)
    return True
        
def get_current_time():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def execmd(cmdString):
    status, output = commands.getstatusoutput(cmdString)
    return status, output

def check_json(jsonStr):
    ret = True
    try:
        json.loads(jsonStr)
    except ValueError, ex:
        ret = False
    return ret

def decode_json(jsonStr):
    return json.loads(jsonStr)

def encode_json(list_json):
    return json.dumps(list_json)

def get_pid_list(procName):
    shell_cmd = 'ps -x'
    status, output = execmd(shell_cmd)
    lines = output.split('\n')
    list_pid = []
    for line in lines:
        if procName in line:
            pid = line.strip().split(' ')[0].strip()
            list_pid.append(int(pid))
    return list_pid

def http(url, params = None, mtimeout = 10, user = None, pwd = None):
    if user and pwd:
        #auth
        base64String = base64.encodestring("%s:%s" % (user, pwd))
        authheader =  "Basic %s" % base64String
        request = urllib2.Request(url)
        request.add_header("Authorization", authheader)
        response = urllib2.urlopen(request)
        return response.code, response.read()
    else:
        data = None
        if params:
            data = urllib.urlencode(params)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(url = request, timeout = mtimeout)
        return response.code, response.read()

def time_stamp_from(orig_time = None):
    cur_time = time.time()
    diff_time = 0
    if orig_time:
        time_arr = time.strptime(orig_time, "%Y-%m-%d %H:%M:%S")
        orig_time = int(time.mktime(time_arr))
        diff_time = int( (cur_time - orig_time)  * 100)
    else:
        diff_time = int(cur_time * 100 )
    return diff_time

def try_reload(module_name):
    try:
        reload(module_name)
    except Exception, ex:
        pass

def write_file(file, content, is_append = False):
    way = 'w+'
    if is_append:
        way = 'a+'
    try:
        fd = open(file, way)
        fd.write(content)
        fd.close()
        return True
    except:
        return False

def get_file_content(file):
    fd = open(file, 'r')
    file_content = fd.read()
    fd.close()
    return file_content

def filter(str):
    ret = str.replace("&amp;", "&")
    return ret
