import substitutor3000

import unittest

class TestSubstitutor3000(unittest.TestCase):
	def test1(self):
		sbst = substitutor3000.Substitutor3000()
		sbst.put("k1", "v1")
		sbst.put("k2", "v2")
		sbst.put("keys", "1: ${k1}, 2: ${k2}")
        	self.assertEqual("1: v1, 2: v2", sbst.get("keys"))

	def test2(self):
		sbst = substitutor3000.Substitutor3000()
		sbst.put("k1", "v1")
		sbst.put("keys", "1: ${k1}, 2: ${k2}")
        	self.assertEqual("1: v1, 2: ", sbst.get("keys"))

	def test3(self):
		sbst = substitutor3000.Substitutor3000()
		sbst.put("k1", "v1")
		sbst.put("keys", "1: ${k1}, 2: ${k1}")
        	self.assertEqual("1: v1, 2: v1", sbst.get("keys"))

	def test4(self):
		sbst = substitutor3000.Substitutor3000()
		sbst.put("k1", "3")
		sbst.put("k2", "45")
		sbst.put("keys", "12${k3}${k1}${k2}")
        	self.assertEqual("12345", sbst.get("keys"))

	def test5(self):
		sbst = substitutor3000.Substitutor3000()
		sbst.put("k1", "v1")
		sbst.put("k2", "v2")
		sbst.put("k1", "v3")
		sbst.put("keys", "${k1}${k2}")
        	self.assertEqual("v3v2", sbst.get("keys"))		

if __name__ == "__main__":
	unittest.main()
