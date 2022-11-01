# 02/11/2022
# Created by Sezgin YILDIRIM

from fastecdsa import keys, curve
from fastecdsa.point import Point
from random import randint
import bit
import sys

class ECDSA:
	def __init__(self):
		self.k = int(curve.secp256k1.q) + 1

	def add(self, n, Q):
		n = keys.get_public_key(n, curve.secp256k1)
		p = self.k * Q + n
		return p

	def ext(self, n, Q):
		n = keys.get_public_key(n, curve.secp256k1)
		p = self.k * Q - n
		return p

	def compress(self, pub):
		if pub.y % 2 == 0:
			y = '02'
		else:
			y = '03'
		return y + hex(pub.x)[2:].zfill(64)

	def point(self, pub_hex):
		x = int(pub_hex[2:66], 16)
		if len(pub_hex) < 70:
			y = bit.format.x_to_y(x, int(pub_hex[:2], 16) % 2)
		else:
			y = int(pub_hex[66:], 16)
		return Point(x, y, curve=curve.secp256k1)

class Proc:
	def __init__(self, public, bits):
		self.public, self.bits = public, 2**bits
		self.main()

	def extract(self):
		p, n = [], []
		for i in range(1000):
			r = randint(self.bits//2, self.bits)
			g = keys.get_public_key(r, curve.secp256k1)
			p.append(str(hex(g.x))[-30:]), n.append(r)
		return p, n
			
	def found(self, priv):
		fo = keys.get_public_key(priv, curve.secp256k1)
		if ecdsa.compress(fo) == self.public:
			print(f'Public Key  : {ecdsa.compress(fo)}')
			print(f'Private Key : {hex(priv)[2:]}')
			sys.exit()

	def main(self):
		pubs, no = self.extract()
		self.public_key = ecdsa.point(self.public)
		while True:
			z = randint(1,self.bits//2)
			p = ecdsa.add(z, self.public_key)
			for i in range(1000):
				if str(hex(ecdsa.add(i, p).x))[-30:] in pubs: self.found(no[pubs.index(str(hex(ecdsa.add(i, p).x))[-30:])] - z - i)
				if str(hex(ecdsa.ext(i, p).x))[-30:] in pubs: self.found(no[pubs.index(str(hex(ecdsa.ext(i, p).x))[-30:])] - z + i)

if __name__ == "__main__":
	public = '0387dc70db1806cd9a9a76637412ec11dd998be666584849b3185f7f9313c8fd28'
	bits = 31
	ecdsa = ECDSA()
	Proc(public, bits)
