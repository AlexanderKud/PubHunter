# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
import secp256k1 as ice
import bit
import sys

class Proc:
	def __init__(self, quit, foundit):
		self.quit, self.foundit = quit, foundit
		self.public, self.bits, self.bf = '02ceb6cbbcdbdf5ef7150682150f4ce2c6f4807b349827dcdbdd1f2efa885a2630', 2**120, 2**23
		self.n = ice.pub2upub('0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798')
		self.main()

	def extract(self):
		p, self.no = [], []
		for i in range(self.bf):
			r = randint(self.bits//2, self.bits)
			p.append(ice.scalar_multiplication(r)), self.no.append(r)
		_bits, _hashes, _bf = ice.Fill_in_bloom(p, 0.000001)
		del p
		#ice.dump_bloom_file("my_bloom_file.bin", _bits, _hashes, _bf)
		return _bits, _hashes, _bf

	def found(self, priv, x):
		for n in self.no:
			private = n + priv if x == 's' else n - priv
			if ice.scalar_multiplication(private) == self.public_key:
				private_key = f'Private Key : {hex(private)[2:]}'
				open('found.txt', 'a').write(str(private_key) + '\n')
				print(private_key)
				self.foundit.set()
		

	def main(self):
		self.public_key = ice.pub2upub(self.public)
		_bits, _hashes, _bf = self.extract()
		while not self.quit.is_set():
			z = randint(1,self.bits//6)
			print(hex(z))
			r = ice.scalar_multiplication(z)
			a = ice.point_addition(self.public_key, r)
			s = ice.point_subtraction(self.public_key, r)
			for i in range(self.bf):
				a = ice.point_addition(a, self.n)
				s = ice.point_subtraction(s, self.n)
				"""
				"""
				if ice.check_in_bloom(a, _bits, _hashes, _bf):
					self.found(z + i + 1, 'a')
					break

				if ice.check_in_bloom(s, _bits, _hashes, _bf):
					self.found(z + i + 1, 's')
					break

				
if __name__ == "__main__":
	quit = mp.Event()
	foundit = mp.Event()
	for i in range(4):
		p = mp.Process(target=Proc, args=(quit, foundit))
		p.start()
	foundit.wait()
	quit.set()
