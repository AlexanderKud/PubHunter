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

#public_key = p2c(public_key)
#print(public_key)

def bloom():
	p = []
	for i in range(1, 2**N):
		p.append(SM(i))
	_bits, _hashes, _bf = BL(p, 0.000001)
	return _bits, _hashes, _bf, p

def bList(bit, bitRange):
	bitList = []
	for i in range(bitRange-5):
		bit = bit // 2
		bitList.append(bit)
	return bitList

def RUN(j,q, f, _bits, _hashes, _bf, p, bitList, N, publicKEY):
	#print(j)
	while not q.is_set():
		pKEY = publicKEY
		count = []
		for B in bitList:
			if randint(0, 1) == 1:
				count.append(B)
				pKEY = PS(pKEY, SM(B))
				if CB(pKEY, _bits, _hashes, _bf):
					print(f'{j} -> join')
					if pKEY in p:
						for i in range(1, 2**N):
							if SM(i) == pKEY:
								break
						if SM(sum(count) + i) == publicKEY:
							print(f'Private KEY ==> {hex(sum(count) + i).upper()}')
						print('JOINJOIN')
						f.set()

if __name__ == '__main__':
	public_key = '03f46f41027bbf44fafd6b059091b900dad41e6845b2241dc3254c7cdd3c5a16c6'
	publicKEY = p2u(public_key)
	bitRange = 50
	N = 22
	bit = 2**bitRange
	_bits, _hashes, _bf, p = bloom()
	bitList = bList(bit, bitRange)
	q, f = mp.Event(), mp.Event()
	for j in range(4):
		PC = mp.Process(target=RUN, args=(j,q,f,_bits, _hashes, _bf, p, bitList, N, publicKEY))
		PC.start()
	f.wait()
	q.set()
