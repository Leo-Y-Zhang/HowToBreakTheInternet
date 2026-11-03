# How to Break the Internet

A lecture on quantum computing and RSA, given with a co-presenter in October 2026.
It explains how RSA keeps messages private, why factoring a large number is hard
for an ordinary computer, and what Shor's algorithm would change.

## What's here

- `slides.html`: the deck, with the demos built in. Open it in a browser and use
  the arrow keys.
- `demos/`: four Python programs used live in the talk. Standard library only,
  Python 3.8 or newer.
  - `toy_rsa.py`: make a key from two small primes, lock a message, then break it
    by factoring, and see how fast trial division blows up.
  - `shor_by_hand.py`: the classical half of Shor's algorithm, step by step, on N = 15.
  - `quantum_shor_sim.py`: the quantum half, simulated amplitude by amplitude:
    superposition, modular exponentiation, the quantum Fourier transform, a
    measurement, then continued fractions.
  - `make_challenge_number.py`: makes a fresh 2048-bit RSA modulus for the
    audience challenge. It writes the secret primes to `challenge_secret.txt`,
    which git ignores.
- `maths-appendix.md`: the maths behind the slides.

```
cd demos
python3 shor_by_hand.py
python3 toy_rsa.py 101 113
python3 quantum_shor_sim.py
```

## Limits

The simulation is exact but tiny: it tracks every amplitude, so memory doubles
with each qubit. It shows how the algorithm works, not how big a real quantum
computer would need to be.
