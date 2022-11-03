# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
import secp256k1 as ice
import bit
import sys

class ECDSA:

	def compress(self, pub):
		pub = hex(int.from_bytes(pub, "big"))[3:]
		if (int(pub[-1], 16) % 2) == 0:
			y = '02'
		else:
			y = '03'
		return y + str(pub[:64])

class Proc:
	def __init__(self, quit, foundit):
		self.quit, self.foundit = quit, foundit
		self.public, self.bits, self.bf = '03a2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4', 2**40, 2**10
		self.n = ice.pub2upub('0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798')
		self.main()

	def extract(self):
		p, n = [], []
		for i in range(self.bf):
			r = randint(self.bits//2, self.bits)
			p.append(ice.scalar_multiplication(r)), n.append(r)
		return p, n

	def found(self, priv):
		private_key = f'Private Key : {hex(priv)[2:]}'
		open('found.txt', 'a').write(str(private_key) + '\n')
		print(private_key)
		self.foundit.set()

	def main(self):
		self.public_key = ice.pub2upub(self.public)
		pubs, no = self.extract()
		while not self.quit.is_set():
			z = randint(1,self.bits//4)
			r = ice.scalar_multiplication(z)
			a = ice.point_addition(self.public_key, r)
			s = a
			for i in range(1024):
				a = ice.point_addition(a, self.n)
				if a in pubs: self.found(no[pubs.index(a)] - i - z - 1)
				if s in pubs: self.found(no[pubs.index(s)] + i - z + 1)
				s = ice.point_subtraction(s, self.n)
				
if __name__ == "__main__":
	quit = mp.Event()
	foundit = mp.Event()
	for i in range(4):
		p = mp.Process(target=Proc, args=(quit, foundit))
		p.start()
	foundit.wait()
	quit.set()
