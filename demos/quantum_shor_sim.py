#!/usr/bin/env python3
"""A complete simulation of the quantum part of Shor's algorithm, amplitude by
amplitude, in pure Python. Slow and small, but it is the real thing: a
superposition over all x, the modular exponentiation, the quantum Fourier
transform, a random measurement, then continued fractions and HCF.

    python3 quantum_shor_sim.py          # N=15, a=7
    python3 quantum_shor_sim.py 21 2     # N=21, a=2  (period 6: Q/r is not a whole number)
    python3 quantum_shor_sim.py 35       # N=35, random a, retries until it works

N up to about 60 runs in a few seconds. No dependencies. Python 3.8+.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # the bar chart uses block characters

import sys, cmath, math, random
from math import gcd
from fractions import Fraction

def fft(a):
    """Iterative radix-2 FFT on a list of complex numbers (length a power of 2).
    The quantum Fourier transform on the first register is exactly this, up to
    the 1/sqrt(Q) normalisation."""
    n = len(a)
    a = list(a)
    j = 0
    for i in range(1, n):                      # bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w = cmath.exp(2j * math.pi / length)
        for start in range(0, n, length):
            wk = 1
            for k in range(length // 2):
                u = a[start + k]
                v = a[start + k + length // 2] * wk
                a[start + k] = u + v
                a[start + k + length // 2] = u - v
                wk *= w
        length <<= 1
    return a

def quantum_period_finding(a, N, verbose=True):
    n = 2 * N.bit_length()                     # enough qubits that Q >= N^2
    Q = 1 << n
    if verbose:
        print(f"  First register: {n} qubits, Q = 2^{n} = {Q} basis states, all in superposition.")
    # State after computing f(x) = a^x mod N into the second register:
    #   (1/sqrt(Q)) sum_x |x>|f(x)>
    # Group amplitudes by the second-register value; the QFT acts on each group independently.
    groups = {}
    for x in range(Q):
        v = pow(a, x, N)
        groups.setdefault(v, [0j] * Q)[x] = 1 / math.sqrt(Q)
    if verbose:
        print(f"  Second register takes {len(groups)} distinct values -> the period is {len(groups)}.")
        print(f"  (The computer cannot read that off; it must find it by interference.)")
    # Apply the QFT to the first register (for every second-register value at once).
    probs = [0.0] * Q
    for v, amps in groups.items():
        out = fft(amps)
        for y in range(Q):
            probs[y] += abs(out[y] / math.sqrt(Q)) ** 2
    if verbose:
        show_bars(probs, Q)
    # Measure the first register.
    y = random.choices(range(Q), weights=probs)[0]
    if verbose:
        print(f"  Measured y = {y}  (probability {probs[y]:.3f})")
    # Continued fractions: y/Q is close to k/r with r < N.
    frac = Fraction(y, Q).limit_denominator(N)
    r = frac.denominator
    if verbose:
        print(f"  y/Q = {y}/{Q} is close to {frac}  ->  candidate period r = {r}")
    return r

def show_bars(probs, Q, width=60):
    """ASCII bar chart of the measurement probabilities, showing the spikes."""
    step = max(1, Q // width)
    peak = max(probs)
    print("  Probability of each measurement outcome after the QFT (spikes = the rhythm):")
    line = ""
    for i in range(0, Q, step):
        p = max(probs[i:i + step])
        h = int(round(8 * p / peak)) if peak else 0
        line += " ▁▂▃▄▅▆▇█"[h]
    print("  " + line)
    print(f"  0{' ' * (len(line) - 2)}{Q}")

def shor(N, a=None, verbose=True):
    for attempt in range(1, 20):
        aa = a if a is not None else random.randrange(2, N - 1)
        print(f"Attempt {attempt}: a = {aa}")
        g = gcd(aa, N)
        if g != 1:
            print(f"  Lucky: HCF({aa}, {N}) = {g}.  {N} = {g} x {N // g}")
            return g, N // g
        r = quantum_period_finding(aa, N, verbose)
        if pow(aa, r, N) != 1:
            print(f"  {aa}^{r} mod {N} != 1, so {r} is not the period (a measurement near, not on, a spike). Retry.")
        elif r % 2:
            print(f"  Period {r} is odd. Retry.")
        else:
            yv = pow(aa, r // 2, N)
            if yv == N - 1:
                print(f"  a^(r/2) = N - 1, the unlucky case. Retry.")
            else:
                p, q = gcd(yv - 1, N), gcd(yv + 1, N)
                print(f"  r = {r} is even. a^(r/2) mod N = {yv}. HCF({yv - 1}, {N}) = {p}, HCF({yv + 1}, {N}) = {q}")
                if 1 < p < N:
                    print(f"\n  {N} = {p} x {N // p}")
                    return p, N // p
                print("  Trivial factors. Retry.")
        if a is not None:
            a = None
    return None

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:] if x.isdigit()]
    N = nums[0] if nums else 15
    a = nums[1] if len(nums) > 1 else (7 if N == 15 else None)
    shor(N, a)
