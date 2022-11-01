"""
02/11/2022
by Sezgin YILDIRIM

"""


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

class Utils:
	def read(self):
		with open('pubs.txt', 'r', encoding='utf-8') as f:
			done = f.readlines()
		f.close()
		return [elem.split()[0] for elem in done]

class Proc:
	def __init__(self):
		self.public = '033c4a45cbd643ff97d77f41ea37e843648d50fd894b864b0d52febc62f6454f7c'
		self.main()

	def extract(self):
		p, n = [], []
		for i in range(1000):
			r = randint(0x80000, 0xFFFFF)
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
			z = randint(1,524287)
			p = ecdsa.add(z, self.public_key)
			for i in range(1000):
				if str(hex(ecdsa.add(i, p).x))[-30:] in pubs: self.found(no[pubs.index(str(hex(ecdsa.add(i, p).x))[-30:])] - z - i)
				if str(hex(ecdsa.ext(i, p).x))[-30:] in pubs: self.found(no[pubs.index(str(hex(ecdsa.ext(i, p).x))[-30:])] - z + i)

if __name__ == "__main__":
	utils = Utils()
	ecdsa = ECDSA()
	Proc()
