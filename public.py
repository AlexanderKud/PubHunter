# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
from ice.secp256k1 import (
	scalar_multiplication as SM,
	Fill_in_bloom as bloom,
	pub2upub as p2u,
	point_addition as PA,
	point_subtraction as PS,
	check_in_bloom as CB)

class Proc:
	def __init__(self, quit, foundit, public_key, bit_range, bloom_range, N_range):
		self.public_key, self.bit_range, self.bloom_range, self.N_range = \
			public_key, bit_range, bloom_range, N_range
		self.main(quit, foundit)

	def bloom(self):
		p, self.no = [], []
		for i in range(self.bloom_range):
			r = randint(self.bit_range//2, self.bit_range)
			p.append(SM(r)), self.no.append(r)
		self._bits, self._hashes, self._bf = bloom(p, 0.000001)
		del p

	def collision(self, priv, foundit):
		for n in self.no:
			private = n + priv
			for j in range(2):
				if SM(private) == self.P:
					private_key = f'Private Key : {hex(private)[2:]}'
					open('found.txt', 'a').write(str(private_key) + '\n')
					print('-'*40 + f'\nKEY FOUND = {private_key}\n' + '-'*40)
					foundit.set()
					return True
				private = n - priv

	def main(self, quit, foundit):
		self.n = SM(1)
		self.P = p2u(self.public_key)
		self.bloom()
		while not quit.is_set():
			rand = randint(1,self.bit_range//4)
			print(hex(rand))
			rand_p = SM(rand)
			add = PA(self.P, rand_p)
			sub = PS(self.P, rand_p)
			for i in range(self.N_range):
				add, sub = PA(add, self.n), PS(sub, self.n)
				if CB(add, self._bits, self._hashes, self._bf) or CB(sub, self._bits, self._hashes, self._bf):
					if self.collision(rand + i + 1, foundit) == True: break

	
if __name__ == "__main__":
	cpu_count = 4
	bit_range = 2**40
	bloom_range = 2**20 // cpu_count
	N_range = 2**20
	public_key = '03a2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4'
	quit = mp.Event()
	foundit = mp.Event()
	for i in range(cpu_count):
		pc = mp.Process(target=Proc, args=(quit, foundit, public_key, bit_range, bloom_range, N_range))
		pc.start()
	foundit.wait()
	quit.set()
