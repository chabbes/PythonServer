# -*- coding: utf-8 -*-

import re

class Substitutor3000(object):
	def __init__(self):
		self.data = {}

	def put(self, key, value):
		self.data[key] = value

	def get(self, key):
		if key not in self.data:
			return ""
		return self.handle(self.data[key])

	def handle(self, s):
		p = re.compile("\\$\\{(.+?)\\}")
		lst = p.findall(s)
		for i in lst:
			if i not in self.data:
				tok = ""
			else:
				tok = self.data[i]
			tmp = "\\$\\{" + i + "\\}"
			p = re.compile(tmp)
			s = p.sub(tok, s)
		return s
