# Live demos (all pure Python, no installs)

Run any of these in a terminal with a big font (Ctrl + = a few times). They need Python 3.8 or newer and nothing else, so they work on any laptop.

| Script | What it shows | Where in the talk |
|---|---|---|
| `shor_by_hand.py` | The classical half of Shor: the rhythm of aˣ mod N, the period, HCF, factors. `--slow` paces it for the stage. | Slides 18–19 (alternative to the JS demo), or Q&A |
| `quantum_shor_sim.py` | The quantum half, simulated exactly: superposition over all x, the QFT, an ASCII bar chart of the spikes, a random measurement, continued fractions, factors. | Slide 21 in the 40-minute version, or Q&A ("can we see the real thing?") |
| `toy_rsa.py` | Builds a real RSA padlock from two small primes, locks "HELLO", then breaks it by factoring. `--growth` times trial division as N grows. | Appendix slide A1, or Q&A |
| `make_challenge_number.py` | Generates a fresh 617-digit N and its two primes for the sealed-envelope trick. | Before the talk (see delivery guide) |

Suggested live sequence for a Q&A "show us the code" moment (two minutes):

```
python3 shor_by_hand.py 15 7
python3 quantum_shor_sim.py 15 7
python3 quantum_shor_sim.py 21 2
```

`challenge_secret.txt` is ignored by git on purpose. Keep it that way.
