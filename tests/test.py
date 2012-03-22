import unittest
import pycpuid

class test_pycpuid(unittest.TestCase):
	def test_vendor(self):
		self.assert_(isinstance(pycpuid.vendor(), basestring))
		self.assertEqual(len(pycpuid.vendor()), 12)
		
if __name__ == "__main__":
	unittest.main()
