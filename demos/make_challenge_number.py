#!/usr/bin/env python3
"""Generate a fresh RSA-2048-sized challenge number for the "sealed envelope"
stage trick. Writes:

    challenge_public.txt   the 617-digit number N (pin this on the noticeboard)
    challenge_secret.txt   the two primes (seal these in an envelope; never commit)

    python3 make_challenge_number.py          # 1024-bit primes (617-digit N)
    python3 make_challenge_number.py 64       # small demo: 64-bit primes

No dependencies. Python 3.8+.
"""
import sys, secrets, random

def is_probable_prime(n, rounds=40):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):                  # Miller-Rabin
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_prime(bits):
    while True:
        c = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(c):
            return c

if __name__ == "__main__":
    bits = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
    p, q = gen_prime(bits), gen_prime(bits)
    N = p * q
    with open("challenge_public.txt", "w") as f:
        f.write(f"Which two primes multiply to make this {len(str(N))}-digit number?\n\n{N}\n")
    with open("challenge_secret.txt", "w") as f:
        f.write(f"p = {p}\nq = {q}\n\nDo not commit this file.\n")
    print(f"N has {len(str(N))} digits ({N.bit_length()} bits).")
    print("Wrote challenge_public.txt and challenge_secret.txt")
