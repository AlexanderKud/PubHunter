# 17/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as MP
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

def bloom(N):
	BELOW = [SM(I)[1:33] for I in range(1, N)]
	bits, hashes, bf = BL(BELOW, 0.000001)
	return bits, hashes, bf, BELOW

def above(bit, bitRange):
	ABOVE = []
	for I in range(bitRange-5):
		bit = bit // 2
		ABOVE.append(bit)
	return ABOVE

def sub(P, bitRange, FIRST):
	KeysP, KeysI, bit, FIRST, N = [], [], 2**(bitRange-2), SM(FIRST), 2**10
	for I in range(N):
		R = randint(1, bit)
		A = SM(R)
		AR = PA(P, A)
		RA = PS(P, A)
		KeysP.append(PS(AR, FIRST))
		KeysP.append(PS(RA, FIRST))
		KeysI.append(R)
	return KeysP, KeysI

class Multi:
	def __init__(self, Q, F, bits, hashes, bf, BELOW, ABOVE, N, P, KeysP, KeysI, FIRST):
		self.Q, self.F, self.bits, self.hashes, self.bf, self.BELOW, \
		self.ABOVE, self.N, self.P, self.KeysP, self.KeysI, self.FIRST = \
		Q, F, bits, hashes, bf, BELOW, ABOVE, N, P, KeysP, KeysI, FIRST
		self.main()

	def found(self, RIP, CC):
		if RIP in self.BELOW:
			print('JOINJOINJOIN')
			for I in range(1, self.N):
				if SM(I)[1:33] == RIP:
					break

			for R in self.KeysI:
				SUM = sum(CC) + self.FIRST + I
				TETRAGRAMMATON = [abs(SUM + R), abs(SUM - R), abs(SUM + R - I*2), abs(SUM - R - I*2)]
				for YHVH in TETRAGRAMMATON:
					if SM(YHVH) == self.P:
						F = f'\n{"*"*80}\nPrivate KEY : 0x{hex(YHVH)[2:].zfill(64).upper()}\
							\nPublic KEY  : {p2c(SM(YHVH)).upper()}\n{"*"*80}'
						print(F), open('found.txt', 'a').write(F)
						self.F.set(), sys.exit()

	def main(self):
		while not self.Q.is_set():
			AC = [A for A in self.ABOVE if randint(0, 1) == 1]
			for i in AC:
				print(hex(i))
			for RIP in self.KeysP:
				CC = []
				for C in AC:
					CC.append(C)
					RIP = PS(RIP, SM(C))
					if CB(RIP[1:33], self.bits, self.hashes, self.bf):
						print('JOIN')
						self.found(RIP[1:33], CC)
						
if __name__ == '__main__':
	public_key = '02ceb6cbbcdbdf5ef7150682150f4ce2c6f4807b349827dcdbdd1f2efa885a2630'
	bitRange = 120
	N = 5000000
	bit = 2**bitRange
	P = p2u(public_key)
	ABOVE = above(bit, bitRange)
	FIRST = ABOVE[0]
	KeysP, KeysI = sub(P, bitRange, FIRST)
	bits, hashes, bf, BELOW = bloom(N)
	ABOVE.pop(0)
	#######################
	Q, F = MP.Event(), MP.Event()
	for j in range(4):
		PC = MP.Process(target=Multi, args=(Q, F, bits, hashes, bf, BELOW, ABOVE, N, P, KeysP, KeysI, FIRST))
		PC.start()
	F.wait()
	Q.set()
