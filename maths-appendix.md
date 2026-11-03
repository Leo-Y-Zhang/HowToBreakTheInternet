# The maths behind the talk (GCSE level, with an A-level extension)

Everything in the talk uses four things you already know: remainders, powers, highest common factor (HCF), and the difference of two squares. This appendix shows the working.

## 1. Remainders ("mod")

"a mod N" means the remainder when a is divided by N.

- 17 mod 15 = 2 (17 = 1 × 15 + 2)
- 49 mod 15 = 4 (49 = 3 × 15 + 4)
- 91 mod 15 = 1 (91 = 6 × 15 + 1)

Two numbers are called *congruent* mod N if they have the same remainder. We write 49 ≡ 4 (mod 15).

Useful fact: you can take remainders at every step of a multiplication and get the same final remainder. So to work out 7⁴ mod 15 you never need to compute 2401; you go 7 → 49 → 4 → 28 → 13 → 91 → 1.

## 2. The rhythm: powers of a, mod N

Take N = 15 and a = 7:

| x | 7ˣ | 7ˣ mod 15 |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 7 | 7 |
| 2 | 49 | 4 |
| 3 | 343 | 13 |
| 4 | 2401 | 1 |
| 5 | 16807 | 7 |
| 6 | | 4 |
| 7 | | 13 |
| 8 | | 1 |

The remainders repeat: 1, 7, 4, 13, 1, 7, 4, 13, ... The length of the repeat is called the **period** (or **order**) of a mod N. Here r = 4.

It always repeats, and it always comes back to 1 first (as long as a and N share no common factor), because there are only N possible remainders and multiplying by a is reversible mod N.

## 3. Why the period gives the factors

We found 7⁴ ≡ 1 (mod 15). That means 7⁴ − 1 is a multiple of 15.

Now, 7⁴ − 1 is a difference of two squares:

  7⁴ − 1 = (7²)² − 1² = (7² − 1)(7² + 1) = 48 × 50 = 2400

and 2400 = 160 × 15. So 15 divides 48 × 50.

15 = 3 × 5. For 15 to divide 48 × 50, the 3 and the 5 have to be somewhere in 48 × 50. Two things can happen:

- Both go into the same bracket (48 or 50 is itself a multiple of 15). Unlucky; try another a.
- They split: one bracket has the 3, the other has the 5. Then HCF(48, 15) and HCF(50, 15) pick them out.

Here: HCF(48, 15) = 3 and HCF(50, 15) = 5. Done.

**General recipe (Shor's classical part):**

1. Pick a random a between 2 and N − 1. If HCF(a, N) > 1 you have a factor already (very lucky).
2. Find the period r: the smallest r ≥ 1 with aʳ ≡ 1 (mod N). *This is the step the quantum computer does.*
3. If r is odd, go back to 1.
4. Compute y = a^(r/2) mod N. If y ≡ −1 (mod N) (i.e. y = N − 1), go back to 1.
5. The factors are HCF(y − 1, N) and HCF(y + 1, N).

Shor proved that for a random a, steps 3 and 4 fail less than half the time, so a handful of tries is enough.

## 4. Worked example 2: N = 21, a = 2

2, 4, 8, 16, 32 mod 21 = 11, 22 mod 21 = 1. Period r = 6.
r/2 = 3, 2³ = 8. HCF(7, 21) = 7, HCF(9, 21) = 3. So 21 = 3 × 7.

## 5. A failure, so you believe the "retry" step: N = 15, a = 14

14 ≡ −1 (mod 15), so 14² ≡ 1. Period r = 2. r/2 = 1, y = 14 = N − 1. That's the "y ≡ −1" case: (14 − 1)(14 + 1) = 13 × 15, and 15 is entirely inside one bracket. HCF(13, 15) = 1 and HCF(15, 15) = 15: useless. Pick another a.

## 6. Exercises (answers at the end)

1. Find the period of 2 mod 15 and use it to factor 15.
2. Find the period of 4 mod 15. It is very short. Does the recipe still work?
3. Find the period of 3 mod 35 and factor 35.
4. Why can't the period of a mod N be bigger than N?
5. (Harder) 3977 = 41 × 97. Without a computer, find the period of 2 mod 3977 by hand... no, don't. Instead explain in one sentence why a normal computer finds this hard when N has 617 digits.

## 7. How RSA actually uses the primes (toy example)

You don't need this for the talk, but it's satisfying. Standard example with small primes:

- Choose primes p = 61, q = 53. N = p × q = 3233.
- Compute φ = (p − 1)(q − 1) = 60 × 52 = 3120.
- Choose e = 17 (any number sharing no factor with 3120).
- Find d with e × d ≡ 1 (mod 3120): d = 2753 (check: 17 × 2753 = 46801 = 15 × 3120 + 1).
- **Public key** (the padlock): (N, e) = (3233, 17). **Private key**: d = 2753, which you can only compute if you know p and q (because you need φ).

Encrypt the message m = 65: c = 65¹⁷ mod 3233 = 2790.
Decrypt: 2790²⁷⁵³ mod 3233 = 65.

An attacker who can factor 3233 into 61 × 53 recomputes φ and d in a second. An attacker who cannot factor N is stuck. `demos/toy_rsa.py` does all of this and then breaks it.

## 8. A-level extension: how interference finds the period

*(Beyond GCSE; for the physics and further-maths crowd.)*

Use n qubits so Q = 2ⁿ ≥ N². Put them in an equal superposition of all x from 0 to Q − 1, and compute aˣ mod N into a second register:

  (1/√Q) Σₓ |x⟩ |aˣ mod N⟩

Because aˣ mod N has period r, the x values that share the same second-register value form a comb: x₀, x₀ + r, x₀ + 2r, ... Apply the quantum Fourier transform to the first register:

  |x⟩ → (1/√Q) Σ_y e^(2πi xy/Q) |y⟩

A comb with spacing r turns into a comb with spacing Q/r: the amplitudes for y near multiples of Q/r add up in phase (constructive interference); all others cancel. Measuring gives y ≈ kQ/r for some k. The fraction y/Q ≈ k/r, and the continued-fraction algorithm recovers r (it works because Q ≥ N² makes k/r the unique fraction with denominator < N that close to y/Q).

The reason this beats a classical computer: the QFT on n qubits uses about n² gates (n ≈ 4100 for RSA-2048 with Q ≥ N²), whereas classically you'd need to look at a number of values of x comparable to r, which is around N.

`demos/quantum_shor_sim.py` simulates exactly this, amplitude by amplitude, for N = 15 and N = 21.

## Answers

1. 2, 4, 8, 1: period 4. 2² = 4. HCF(3, 15) = 3, HCF(5, 15) = 5.
2. 4, 1: period 2. y = 4¹ = 4. HCF(3, 15) = 3, HCF(5, 15) = 5. Yes, it works: the only failure cases are an odd period or y = N − 1, and 4 ≠ 14.
3. 3, 9, 27, 81 mod 35 = 11, 33, 99 mod 35 = 29, 87 mod 35 = 17, 51 mod 35 = 16, 48 mod 35 = 13, 39 mod 35 = 4, 12, 36 mod 35 = 1. Period 12. 3⁶ mod 35 = 29. HCF(28, 35) = 7, HCF(30, 35) = 5.
4. There are only N possible remainders, so the sequence must repeat within N steps.
5. Because the period can be as long as N itself (hundreds of digits), and the only classical way to find it is essentially to walk along the pattern one step at a time.
