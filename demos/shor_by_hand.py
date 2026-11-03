#!/usr/bin/env python3
"""Shor's algorithm, the classical half, step by step.

Shows the "rhythm" (powers of a mod N), finds the period, and turns it into
factors using only remainders, powers and HCF. Run it live in a terminal:

    python3 shor_by_hand.py            # N=15, a=7 (the example in the talk)
    python3 shor_by_hand.py 21 2       # N=21, a=2
    python3 shor_by_hand.py 3977       # pick a at random, retry until it works
    python3 shor_by_hand.py 3977 --slow   # pause between steps for the stage

No dependencies. Python 3.8+.
"""
import sys, time, random
from math import gcd

SLOW = "--slow" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]

def pause(t=0.8):
    if SLOW:
        time.sleep(t)

def say(msg=""):
    print(msg)
    pause(0.5)

def find_period(a, N, show=True):
    """Walk along a^x mod N until it comes back to 1. Returns the period r."""
    x, value = 1, a % N
    row = [1]
    while value != 1:
        row.append(value)
        value = (value * a) % N
        x += 1
        if show and x <= 40:
            print(f"  {a}^{x-1:<3} mod {N} = {row[-1]}")
            pause(0.15)
    if show and x > 40:
        print(f"  ... ({x - 40} more steps) ...")
    if show:
        print(f"  {a}^{x:<3} mod {N} = 1   <- back to 1")
    return x

def shor_classical(N, a):
    say(f"N = {N}, a = {a}")
    g = gcd(a, N)
    if g != 1:
        say(f"  Lucky: HCF({a}, {N}) = {g} is already a factor. {N} = {g} x {N // g}")
        return g, N // g
    say("Step 1: the rhythm. Keep multiplying by a and wrapping around mod N:")
    r = find_period(a, N)
    say(f"\nStep 2: the pattern repeats every {r} steps. Period r = {r}.")
    if r % 2:
        say(f"  r is odd. Unlucky; pick another a.")
        return None
    half = r // 2
    y = pow(a, half, N)
    say(f"\nStep 3: halve it: r/2 = {half}.  a^(r/2) mod N = {a}^{half} mod {N} = {y}")
    if y == N - 1:
        say(f"  {y} is N - 1, the unlucky case. Pick another a.")
        return None
    say(f"\nStep 4: look either side of {y}: {y - 1} and {y + 1}.")
    p, q = gcd(y - 1, N), gcd(y + 1, N)
    say(f"  HCF({y - 1}, {N}) = {p}")
    say(f"  HCF({y + 1}, {N}) = {q}")
    if 1 < p < N:
        say(f"\n  {N} = {p} x {N // p}")
        return p, N // p
    say("  Trivial factors. Pick another a.")
    return None

def main():
    N = int(args[0]) if args else 15
    a = int(args[1]) if len(args) > 1 else None
    tries = 0
    while True:
        tries += 1
        aa = a if a is not None else random.randrange(2, N - 1)
        print("=" * 60)
        result = shor_classical(N, aa)
        if result:
            print("=" * 60)
            print(f"Factored {N} = {result[0]} x {result[1]} after {tries} attempt(s).")
            print("The quantum computer's only job was step 1-2: finding the period.")
            return
        if a is not None:
            print("Retry with a different a (run again without specifying a).")
            return

if __name__ == "__main__":
    main()
