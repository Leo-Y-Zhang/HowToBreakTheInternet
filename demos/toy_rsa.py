#!/usr/bin/env python3
"""Toy RSA: make a padlock from two primes, lock a message, then break it by
factoring. Then show how fast factoring-by-trial-division blows up.

    python3 toy_rsa.py                # textbook example: p=61, q=53
    python3 toy_rsa.py 101 113        # your own small primes
    python3 toy_rsa.py --growth       # time trial division as N grows

No dependencies. Python 3.8+.
"""
import sys, time, random
from math import gcd, isqrt

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True

def factor_by_trial(N):
    """The attacker's tool: try every possible divisor. Returns (p, q, tries)."""
    tries = 0
    if N % 2 == 0:
        return 2, N // 2, 1
    for d in range(3, isqrt(N) + 1, 2):
        tries += 1
        if N % d == 0:
            return d, N // d, tries
    return None, None, tries

def make_keys(p, q, e=17):
    N = p * q
    phi = (p - 1) * (q - 1)
    while gcd(e, phi) != 1:
        e += 2
    d = pow(e, -1, phi)          # e * d = 1 (mod phi)
    return (N, e), d

def encrypt_text(text, pub):
    N, e = pub
    return [pow(ord(ch), e, N) for ch in text]

def decrypt_blocks(blocks, N, d):
    return "".join(chr(pow(c, d, N)) for c in blocks)

def demo(p, q):
    print(f"Alice picks two primes and keeps them secret:  p = {p}, q = {q}")
    pub, d = make_keys(p, q)
    N, e = pub
    print(f"She publishes the padlock (public key):        N = {N}, e = {e}")
    print(f"She keeps the key (private key):               d = {d}")
    print()
    msg = "HELLO"
    blocks = encrypt_text(msg, pub)
    print(f"Bob locks the message {msg!r} with the padlock:  {blocks}")
    print(f"Alice unlocks it with d:                       {decrypt_blocks(blocks, N, d)!r}")
    print()
    print("Now an attacker who only has the padlock (N, e) and the locked message...")
    t0 = time.perf_counter()
    pp, qq, tries = factor_by_trial(N)
    dt = time.perf_counter() - t0
    print(f"  tries dividing N by 3, 5, 7, ... and after {tries} tries finds N = {pp} x {qq}  ({dt*1000:.2f} ms)")
    phi = (pp - 1) * (qq - 1)
    dd = pow(e, -1, phi)
    print(f"  recomputes the private key: d = {dd}")
    print(f"  and reads the message:      {decrypt_blocks(blocks, N, dd)!r}")
    print()
    print("Small primes: broken in a millisecond. The only defence is making N too big to factor.")

def growth():
    print("How trial division scales. Each extra 10 bits multiplies the work by about 32.")
    print(f"{'bits':>5} {'N':>22} {'divisions':>12} {'time':>10}")
    for bits in (20, 24, 28, 32, 36, 40, 44):
        p = random_prime(bits // 2)
        q = random_prime(bits // 2)
        N = p * q
        t0 = time.perf_counter()
        _, _, tries = factor_by_trial(N)
        dt = time.perf_counter() - t0
        print(f"{bits:>5} {N:>22} {tries:>12} {dt:>9.3f}s")
        if dt > 20:
            break
    print()
    print("Extrapolate: a 2048-bit N would need about 2^1023 divisions.")
    print("That is roughly 10^308 of them. The universe is about 4 x 10^17 seconds old.")
    print("(Real attackers use cleverer methods than trial division, but they hit the same wall a bit later.)")

def random_prime(bits):
    while True:
        c = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(c):
            return c

if __name__ == "__main__":
    if "--growth" in sys.argv:
        growth()
    else:
        nums = [int(a) for a in sys.argv[1:] if a.isdigit()]
        p, q = (nums + [61, 53])[:2]
        assert is_prime(p) and is_prime(q) and p != q, "give two different primes"
        demo(p, q)
