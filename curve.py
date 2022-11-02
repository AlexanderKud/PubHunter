# 02/11/2022
# Created by Sezgin YILDIRIM

from multiprocessing import Process
import secp256k1 as ice
from random import randint
import bit
import sys

class ECDSA:
	def pub2upub(self, pub_hex):
		x = int(pub_hex[2:66],16)
		if len(pub_hex) < 70:
			y = bit.format.x_to_y(x, int(pub_hex[:2],16)%2)
		else:
			y = int(pub_hex[66:],16)
		return bytes.fromhex('04'+ hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

	def compress(self, pub):
		pub = hex(int.from_bytes(pub, "big"))[3:]
		if (int(pub[-1], 16) % 2) == 0:
			y = '02'
		else:
			y = '03'
		return y + str(pub[:64])

class Proc:
	def __init__(self):
		self.public, self.bits, self.bf = '030d282cf2ff536d2c42f105d0b8588821a915dc3f9a05bd98bb23af67a2e92a5b', 2**30, 2**10
		self.main()

	def extract(self):
		p, n = [], []
		for i in range(self.bf):
			r = randint(self.bits//2, self.bits)
			p.append(ice.scalar_multiplication(r)), n.append(r)
		return p, n

	def main(self):
		self.public_key = ECDSA().pub2upub(self.public)
		pubs, no = self.extract()
		while True:
			z = randint(1,self.bits//4)
			print(hex(z))
			r = ice.scalar_multiplication(z)
			p = ice.point_addition(self.public_key, r)
			for i in range(1024):
				p = ice.point_increment(p)
				if p in pubs:
					private_key = f'Private Key : {hex(no[pubs.index(p)] - i - z - 1)[2:]}'
					open('found.txt', 'a').write(str(private_key) + '\n').close()
					print(private_key)
					sys.exit()

class M:
	def multi(self):
		que = []
		for session in range(4):
			que.append(Process(target=Proc, args=( )))
			que[-1].start()

if __name__ == "__main__":
	M().multi()
