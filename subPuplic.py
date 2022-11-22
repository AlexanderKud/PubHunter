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

def sub(P, bitRange):
	KeysP, KeysI, bit, N = [], [], 2**(bitRange-3), 2**10
	bit //= N
	for I in range(1, N):
		R = bit * I
		A = SM(R)
		KeysP.append(PA(P, A))
		KeysP.append(PS(P, A))
		KeysI.append(R)
	return KeysP, KeysI

class Multi:
	def __init__(self, Q, F, bits, hashes, bf, BELOW, N, P, KeysP, KeysI, bit):
		self.Q, self.F, self.bits, self.hashes, self.bf, self.BELOW, \
		self.N, self.P, self.KeysP, self.KeysI, self.bit = \
		Q, F, bits, hashes, bf, BELOW, N, P, KeysP, KeysI, bit
		self.main()

	def found(self, RIP, CC):
		if RIP in self.BELOW:
			self.F.set()
			for I in range(1, self.N):
				if SM(I)[1:33] == RIP:
					break

			for R in self.KeysI:
				SUM = sum(CC) + I
				TETRAGRAMMATON = [abs(SUM + R), abs(SUM - R), abs(SUM + R - I*2), abs(SUM - R - I*2)]
				for YHVH in TETRAGRAMMATON:
					if SM(YHVH) == self.P:
						F = f'\n{"*"*80}\nPrivate KEY : 0x{hex(YHVH)[2:].zfill(64).upper()}\
							\nPublic KEY  : {p2c(SM(YHVH)).upper()}\n{"*"*80}'
						print(F), open('found.txt', 'a').write(F)
						sys.exit()

	def paradigm(self):
		S, B, P = [], 2**(self.bit), randint(2**(self.bit-1), 2**self.bit)
		for A in range(self.bit-5):
			B //= 2
			P -= B
			if P <= 0:
				P += B
			else:
				S.append(B)
		return S

	def main(self):
		while not self.Q.is_set():
			AC = self.paradigm()
			for RIP in self.KeysP:
				CC = []
				for C in AC:
					CC.append(C)
					RIP = PS(RIP, SM(C))
					if CB(RIP[1:33], self.bits, self.hashes, self.bf):
						self.found(RIP[1:33], CC)
						
if __name__ == '__main__':
	public_key = '03f46f41027bbf44fafd6b059091b900dad41e6845b2241dc3254c7cdd3c5a16c6'
	bitRange = 50
	N = 5000000
	P = p2u(public_key)
	KeysP, KeysI = sub(P, bitRange)
	bits, hashes, bf, BELOW = bloom(N)
	#######################
	Q, F = MP.Event(), MP.Event()
	for j in range(4):
		PC = MP.Process(target=Multi, args=(Q, F, bits, hashes, bf, BELOW, N, P, KeysP, KeysI, bitRange))
		PC.start()
	F.wait()
	Q.set()
