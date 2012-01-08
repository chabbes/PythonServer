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
		threading.Thread.__init__(self)

	def run(self):
		time.sleep(self.serv.getSleepTime())
		buf = self.sock.recv(1024)
		inp = string.split(buf)
		res = "Wrong command! "
		if inp[0] == "PUT":
			if len(inp) == 3:
				self.serv.getSbst().put(inp[1], inp[2])
				res = "OK\n"
			else:
				res += "USAGE: PUT key value\n"
		if inp[0] == "GET":
			if len(inp) == 2:
				res = "VALUE\n" + self.serv.getSbst().get(inp[1]) + "\n"
			else:
				res += "USAGE: GET key\n"
		if inp[0] == "SET":
			if len(inp) == 3:
				if inp[1] == "SLEEP":
					try:
						self.serv.setSleepTime(int(inp[2]))
						res = "OK\n"
					except:
						res += "USAGE: SET SLEEP number\n"
				else:
					res += "USAGE: SET SLEEP number\n"
			else:
				res += "USAGE: SET SLEEP number\n"
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
