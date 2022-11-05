# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
import secp256k1 as ice
import sys

##############################################
address = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'

bit = 66            # Range
RANGE = 128         # Stride in every range
cpu_count = 4       # CPU COUNT
##############################################
start = 2**(bit-1)
B = bytes.fromhex(ice.b58_decode(address)[2:-8])
stride = ice.scalar_multiplication(1)

def RUN():
    while not quit.is_set():
        range_smash = randint(16, 64)
        base = start // range_smash
        smash = [start + (base * i) for i in range(range_smash + 1)]
        #for I in range(range_smash): print(hex(smash[I]), hex(smash[I+1]))
        R = randint(1, smash[1] - smash[0])
        for I in range(range_smash):
            #R = randint(smash[I], smash[I+1])
            nail = smash[I] + R
            A = ice.scalar_multiplication(nail)
            S = ice.point_subtraction(A, stride)
            for N in range(RANGE):
                A = ice.point_addition(A, stride)
                S = ice.point_subtraction(S, stride)
                if ice.pubkey_to_h160(0, True, A) == B or ice.pubkey_to_h160(0, True, S) == B:
                    P = hex(nail - N - 2)[2:] if ice.privatekey_to_h160(0, True, nail - N - 2) == B else hex(nail + N + 1)
                    print('#'*30 + f'\nPrivate Key : {P}\n' + '#'*30)
                    open('found.txt', 'a').write('#'*30 + f'\nPrivate Key : {P}\n' + '#'*30 + '\n')
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