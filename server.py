# -*- coding: utf-8 -*-

import substitutor3000

import threading
import time
import socket

import string

class Server(object):
	def __init__(self, sckt):
		self.sckt = sckt
		self.substitutor = substitutor3000.Substitutor3000()
		self.sleepTime = 0

	def getSbst(self):
		return self.substitutor

	def getSleepTime(self):
		return self.sleepTime

	def setSleepTime(self, time):
		self.sleepTime = time

	def run(self):
		while True:
			sock, addr = self.sckt.accept()
			Connection(self, sock, addr).start()

class Connection(threading.Thread):
	def __init__(self, serv, sock, addr):
		self.serv = serv
		self.sock = sock
		self.addr = addr
		self.lock = threading.Lock()
		threading.Thread.__init__(self)

	def PUT(self, inp):
		with self.lock:
			if len(inp) == 3:
				self.serv.getSbst().put(inp[1], inp[2])
				return "OK\n"
			else:
				return "USAGE: PUT key value\n"

	def GET(self, inp):
		with self.lock:
			if len(inp) == 2:
				return "VALUE\n" + self.serv.getSbst().get(inp[1]) + "\n"
			else:
				return "USAGE: GET key\n"
			
	def SET(self, inp):
		if len(inp) == 3:
			if inp[1] == "SLEEP":
				try:
					self.serv.setSleepTime(int(inp[2]))
					return "OK\n"
				except:
					return "USAGE: SET SLEEP number\n"
			else:
				return "USAGE: SET SLEEP number\n"
		else:
			return "USAGE: SET SLEEP number\n"

	def run(self):
		time.sleep(self.serv.getSleepTime())
		buf = self.sock.recv(1024)
		inp = string.split(buf)
		try:
			res = getattr(self, inp[0])(inp)
		except:
			res = "Wrong command!\n"
		self.sock.send(res) 
		self.sock.close()

if __name__ == "__main__":
	host = "localhost"
	port = 9129

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)

	Server(s).run()				
