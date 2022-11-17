# 17/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
from ice.secp256k1 import (
	scalar_multiplication as SM,
	Fill_in_bloom as BL,
	pub2upub as p2u,
	point_addition as PA,
	point_subtraction as PS,
	check_in_bloom as CB,
	point_to_cpub as p2c)
import sys

public_key = '03a2efa402fd5268400c77c20e574ba86409ededee7c4020e4b9f0edbee53de0d4'


publicKEY = p2u(public_key)
#public_key = p2c(public_key)
#print(public_key)

bitRange = 40
N = 17

bit = 2**bitRange

p = []
for i in range(1, 2**N):
	p.append(SM(i))
_bits, _hashes, _bf = BL(p, 0.000001)

bitList = []
for i in range(bitRange-5):
	bit = bit // 2
	bitList.append(bit)

def RUN(q, f):
	while not q.is_set():
		pKEY = publicKEY
		count = []
		for B in bitList:
			R = randint(0, 1)
			if R == 1:
				count.append(B)
				pKEY = PS(pKEY, SM(B))
				if CB(pKEY, _bits, _hashes, _bf):
					print('join')
					if pKEY in p:
						for i in range(1, 2**N):
							if SM(i) == pKEY:
								break
						if SM(sum(count) + i) == publicKEY:
							print(f'Private KEY ==> {hex(sum(count) + i).upper()}')
						print('JOINJOIN')
						f.set()

if __name__ == '__main__':
	q, f = mp.Event(), mp.Event()
	for j in range(4):
		PC = mp.Process(target=RUN, args=(q,f))
		PC.start()
	f.wait()
	q.set()



