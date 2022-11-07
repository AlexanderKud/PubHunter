# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
from ice.secp256k1 import (
    b58_decode as b58,
    privatekey_to_h160 as p2h,
    privatekey_loop_h160_sse as loop)
import sys

class Proc:
	def __init__(self, quit, foundit, public_key, bit_range, bloom_range, N_range):
		self.public_key, self.bit_range, self.bloom_range, self.N_range = \
			public_key, bit_range, bloom_range, N_range
		self.main(quit, foundit)

	def bloom(self):
		p, self.no = [], []
		for i in range(self.bloom_range):
			r = randint(self.bit_range//2, self.bit_range)
			p.append(ice.scalar_multiplication(r)), self.no.append(r)
		self._bits, self._hashes, self._bf = ice.Fill_in_bloom(p, 0.000001)
		del p

	def collision(self, priv, foundit):
		for n in self.no:
			private = n + priv
			for j in range(2):
				if ice.scalar_multiplication(private) == self.P:
					private_key = f'Private Key : {hex(private)[2:]}'
					open('found.txt', 'a').write(str(private_key) + '\n')
					print('-'*40 + f'\nKEY FOUND = {private_key}\n' + '-'*40)
					foundit.set()
					return True
				private = n - priv

	def main(self, quit, foundit):
		self.n = ice.scalar_multiplication(1)
		self.P = ice.pub2upub(self.public_key)
		self.bloom()
		while not quit.is_set():
			rand = randint(1,self.bit_range//4)
			print(hex(rand))
			rand_p = ice.scalar_multiplication(rand)
			add = ice.point_addition(self.P, rand_p)
			sub = ice.point_subtraction(self.P, rand_p)
			for i in range(self.N_range):
				add, sub = ice.point_addition(add, self.n), ice.point_subtraction(sub, self.n)
				if ice.check_in_bloom(add, self._bits, self._hashes, self._bf) or ice.check_in_bloom(sub, self._bits, self._hashes, self._bf):
					if self.collision(rand + i + 1, foundit) == True: break

	
if __name__ == "__main__":
	cpu_count = 4
	bit_range = 2**120
	bloom_range = 2**24 // cpu_count
	N_range = 2**20
	public_key = '02ceb6cbbcdbdf5ef7150682150f4ce2c6f4807b349827dcdbdd1f2efa885a2630'
	quit = mp.Event()
	foundit = mp.Event()
	for i in range(cpu_count):
		pc = mp.Process(target=Proc, args=(quit, foundit, public_key, bit_range, bloom_range, N_range))
		pc.start()
	foundit.wait()
	quit.set()
	sys.exit()