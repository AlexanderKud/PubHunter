# 02/11/2022
# Created by Sezgin YILDIRIM

import multiprocessing as mp
from random import randint
import secp256k1 as ice

##############################################
address = '1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps'

bit = 30            # Range
RANGE = 1024        # Stride in every range
cpu_count = 4       # CPU COUNT
compressed = True   # 'compressed = True' or 'uncompressed = False'
##############################################

_ = 2**(bit-1)
P = bytes.fromhex(ice.b58_decode(address)[2:-8])

def found(x):
    for i in range(RANGE):
        _p, p_ = x + i, x - i
        T = ice.privatekey_to_h160(0, compressed, _p) + ice.privatekey_to_h160(0, compressed, p_)
        if P in T:
            V = hex(_p)[2:] if ice.privatekey_to_h160(0, compressed, _p) == P else hex(p_)
            print('#'*30 + f'\nPrivate Key : {V}\n' + '#'*30)
            open('found.txt', 'a').write('#'*30 + f'\nPrivate Key : {V}\n' + '#'*30 + '\n')
            foundit.set()
            return True

def RUN():
    while not quit.is_set():
        M = randint(16, 64)
        B = _ // M
        S = [_ + (B * i) for i in range(M + 1)]
        R = randint(1, S[1] - S[0])
        for I in range(M):
            K = S[I] + R
            T = ice.privatekey_loop_h160_sse(RANGE, 0, compressed, K) + ice.privatekey_loop_h160_sse(RANGE, 0, compressed, K - RANGE)
            if P in T:
                found(K)
                break

if __name__ == '__main__':
    quit = mp.Event()
    foundit = mp.Event()
    for i in range(cpu_count):
        pc = mp.Process(target=RUN, args=( ))
        pc.start()
    foundit.wait()
    quit.set()
