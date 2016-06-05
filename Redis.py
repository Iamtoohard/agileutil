#coding=utf-8

import redis
import binascii
import ctypes

class RedisHash(object):

	def __init__(self, servers, vNodeCount = 100):
		self._servers = servers
		self._vNodeCount = vNodeCount
		self._serversCount = len(self._servers)	
		self._vNodeHash = {}
		self._badServersIndex = []
		for i in xrange(len(self._servers)):
			server = self._servers[i]
			host = server['host']
			port = server['port']
			for j in xrange(self._vNodeCount):
				key = host + ':' + str(port) + ':' + str(j)
				hash = self._hash(key)
				# hash => index, server[index] is a host and port config
				self._vNodeHash[hash] = i
		self._vNodeHashKeys = self._vNodeHash.keys()
		self._vNodeHashKeys.sort()
		self.curRedisIndex = 0
		self.curVNodeHash = 0		

	def get(self, key):
		redis = self._getRedis(key)
		if redis == False:
			return False
		return redis.get(key)

	def set(self, key, value, expire = -1):
		redis = self._getRedis(key)
		if redis == False:
			return False
		if expire < 0 and expire != -1:
			return False
		if expire == -1:
			return redis.set(key, value)
		else:
			return redis.setex(key, value, expire)

	def _getRedis(self, key):
		"""
		_getRedis is the core method for redis hash, it provide a redis instance according by the key when you called. 
		It will set the value to those redis server on average.Though, the data is storged on every redis server.
	    If the redis server is down, then a available redis server will be returned, when the down server recover, it
		will be push into the normal redis server list to service. Enjoy it! 
		"""

		hasAvaliable = False
		rd = False
		while not hasAvaliable:
			if len(self._badServersIndex) == self._serversCount:
				print 'len(self._badServersIndex) == self._serversCount'
				return False
			hash = self._hash(key)
			vNodeHash = self._getNextHash(hash)
			serverIndex = self._vNodeHash[vNodeHash]
			while (serverIndex in self._badServersIndex):
				print 'while (serverIndex in self._badServersIndex)'
				hash = vNodeHash + 1
				vNodeHash = self._getNextHash(hash)
				serverIndex = self._vNodeHash[vNodeHash]
			server = self._servers[serverIndex]
			print server
			try:
				rd = redis.Redis(host = server['host'], port = server['port'], db = server['db'], password = server['password'])
				rd.ping()
				hasAvaliable = True
				self.curRedisIndex = serverIndex
				self.curVNodeHash = vNodeHash
			except Exception, ex:
				print ex
				self._badServersIndex.append(serverIndex)
		return rd

	def _getNextHash(self, hash):
		maxHash = self._vNodeHashKeys[-1]
		if hash > maxHash:
			return 0
		for h in self._vNodeHashKeys:
			if h >= hash:
				return h

	def _hash(self, str):
		return self._unsigned(binascii.crc32(str))

	def _sortedByDictKey(self, mydict):
		keys = mydict.keys()
		keys.sort()
		return [mydict[key] for key in keys]

	def _unsigned(self, num):
		return ctypes.c_uint64(num).value

	def dump(self):
		a = []
		b = []
		for k,v in self._vNodeHash.items():
			if v == 0:
				a.append(k)
			else:
				b.append(k)
		print len(a)
		print len(b)

		#print self._vNodeHashKeys


if __name__ == '__main__':
	#r = redis.Redis(host='localhost', port=6379, db=0, password='qihoo360')
	serverList = [
		{
			'host'     : '192.168.1.1',
			'port'     : 6379,
			'db'       : 0,
			'password' : '',
		},

		{
			'host'     : '192.168.1.2',
			'port'     : 6379,
			'db'       : 0,
			'password' : '',
		},
	]
	r = RedisHash(serverList)
	for i in xrange(100):
		print r.set(str(i), str(i), 60)
		print r.curRedisIndex
		print r.curVNodeHash
		print "[" + str(i) + "]"

	"""
	print r.get("97")
	print r.curRedisIndex
	print r.curVNodeHash
	"""
