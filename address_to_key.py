import multiprocessing as mp
from random import randint
import secp256k1 as ice
import sys

##############################################
address = '1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum'

bit = 20 		# Range
range_smash = 16 	# Split into intervals
RANGE = 256 		# Stride in every range
cpu_count = 4 		# CPU COUNT
##############################################
start = 2**(bit-1)
base = start // range_smash
smash = [start + (base * i) for i in range(range_smash + 1)]
for I in range(range_smash): print(hex(smash[I]), hex(smash[I+1]))
B = bytes.fromhex(ice.b58_decode(address)[2:-8])
stride = ice.scalar_multiplication(1)

def RUN():
	while not quit.is_set():
		for I in range(range_smash):
			R = randint(smash[I], smash[I+1])
			A = ice.scalar_multiplication(R)
			S = ice.point_subtraction(A, stride)
			for N in range(RANGE):
				A = ice.point_addition(A, stride)
				S = ice.point_subtraction(S, stride)
				if ice.pubkey_to_h160(0, True, A) == B or ice.pubkey_to_h160(0, True, S) == B:
					P = hex(R - N - 2)[2:] if ice.privatekey_to_h160(0, True, R - N - 2) == B else hex(R + N + 1)
					print('#'*30 + f'\nPrivate Key : {P}\n' + '#'*30)
					foundit.set()
					break

if __name__ == '__main__':
	quit = mp.Event()
	foundit = mp.Event()
	for i in range(cpu_count):
		pc = mp.Process(target=RUN, args=( ))
		pc.start()
	foundit.wait()
	quit.set()
