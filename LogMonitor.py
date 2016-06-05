#coding=utf-8

import sys
import time

LOG_FILE = ''
INTERVAL = 60
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2
fd = 0
last_seek = -1

def open_log():
	try:
		global fd
		fd = open(LOG_FILE, 'r')
	except Exception, ex:
		print str(ex)
		sys.exit(1)

def close_log():
	fd.close()

def monitor_log():
	global last_seek
	while True:
		open_log()
		fd.seek(0, SEEK_END)
		if last_seek == -1:
			last_seek = fd.tell()
		else:
			cur_seek = fd.tell()
			size = cur_seek - last_seek
			if size == 0:
				pass
			elif size < 0:
				last_seek = cur_seek
			else:
				fd.seek(last_seek, SEEK_SET)
				text = fd.read(size)
				fd.seek(cur_seek, SEEK_SET)
				last_seek = cur_seek
				call(text)
		time.sleep(INTERVAL)
		close_log()

def call(text):
	print text

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'no log file, usage: log_monitor.py [logFileName] [interval]'
		sys.exit(0)
	LOG_FILE = sys.argv[1]
	if len(sys.argv) == 3:
		INTERVAL = int(sys.argv[2])
	monitor_log()
