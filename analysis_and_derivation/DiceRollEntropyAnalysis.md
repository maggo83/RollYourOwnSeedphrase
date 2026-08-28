# Entropy from ideal and real dice for BIP-39 mnemonics

Document navigation:

- [Overview](../README.md)
- Next: [Expected performance of real six-sided dice](ExpectedDicePerformace.md)

---

## Executive summary

This document compares four factors:

1. ideal versus biased six-sided dice;
2. the number $N$ of physical dice rolled as a batch;
3. direct binary quantization, the variable-length mapping, and base-6 conversion;
4. 12-word (128 entropy bits) versus 24-word (256 entropy bits) BIP-39 mnemonics.

The main conclusions are:

- With no restriction on a real die's probabilities, there is **no positive entropy guarantee**. A permitted distribution is $(1,0,0,0,0,0)$, which has zero entropy. Independence between repeated rolls does not fix a deterministic or nearly deterministic die.
- Shannon entropy and min-entropy answer different questions. Shannon entropy often remains close to ideal despite modest bias, while min-entropy can show a material security loss. Min-entropy is therefore the conservative primary measure; both are reported below.
- For binary quantization, only the group probability
  $$a=p_1+p_2+p_3$$
  matters. Face-level bias can cancel perfectly if $a=1/2$, or it can be amplified if three high-probability faces fall in the same group.
- Base 6 retains up to $\log_2 6\approx2.585$ bits per result, whereas binary quantization deliberately retains at most one bit. Base 6 can therefore provide a larger entropy budget from fewer results, but conversion into exactly 128 or 256 bits must be specified carefully.
- The variable-length mapping sends faces 1–4 to 00, 01, 10, and 11 and faces 5–6 to 0 and 1. With ideal dice it produces uniform bits, uses every result, and needs 77.04 or 153.84 rolls on average including final-boundary overshoot.
- All physical imperfections are represented here only through the final-outcome probability vectors. Their physical causes and empirical size are outside this document's scope.
- The usual range-rejection conversion is exactly unbiased for ideal dice. It is **not** automatically unbiased for real dice. No fixed deterministic conversion can turn every unknown biased distribution into a uniform seed.
- Batch size $N$ mainly changes convenience and the number of physical throws. It gives **no worst-case entropy improvement**: all $N$ dice may have the same aligned bias. If different dice have different biases and their identities really are unobservable, uniform random ordering can improve entropy, but that improvement must not be assumed without a model or measurements.
- A 24-word mnemonic doubles the entropy-bearing input from 128 to 256 bits. It also approximately doubles the absolute entropy loss caused by a fixed per-result bias. The checksum adds no entropy.

The most important mathematical message is that “independent rolls” and “many dice” are not substitutes for a quantitative bound on the final-outcome probabilities.

---

## 1. Scope and assumptions

### 1.1 BIP-39 lengths

BIP-39 uses an initial entropy string of length $L$ and appends a deterministic checksum of length $L/32$. The result is split into 11-bit word indices:

| Mnemonic | Independent entropy $L$ | Checksum | Total encoded bits |
| ---: | ---: | ---: | ---: |
| 12 words | 128 | 4 | 132 |
| 24 words | 256 | 8 | 264 |

Thus a 12-word mnemonic has 128 independently selectable bits, and a 24-word mnemonic has 256 independently selectable bits. The checksum detects some transcription errors but adds no randomness.

### 1.2 Dice model

There are $N$ physical six-sided dice. Die $j$ has a fixed probability vector

$$
\mathbf p_j=(p_{j1},p_{j2},\ldots,p_{j6}),
\qquad p_{ji}\ge0,
\qquad \sum_{i=1}^6p_{ji}=1.
$$

For an ideal die, $p_{ji}=1/6$ for every face. Outcomes of all dice and all repeated throws are assumed statistically independent conditional on the fixed vectors $\mathbf p_j$.

Each vector represents the aggregate distribution of **recorded final outcomes**. This document takes those vectors as inputs and does not decompose their physical causes. Evidence about inherent die imperfections is reviewed in [Expected performance of real six-sided dice](ExpectedDicePerformace.md); effects of the rolling process are analyzed in [Rolling technique and throw dynamics](RollingTechnique.md).

Security calculations conservatively assume an attacker knows the applicable final-outcome probability vectors and the generation procedure. Merely not knowing one's own dice biases is not counted as secret entropy.

### 1.3 Batch ordering model

After a batch is thrown, the physical dice cannot be identified. Their face values are read in an order corresponding to an independent, uniformly random permutation. Only that ordered face sequence is retained; die identities and the permutation are forgotten.

This is the “only ordered face values” model. If an attacker can distinguish scratches, colors, positions, or other identifying features, the permutation benefit disappears and the labeled-dice lower benchmark should be used.

### 1.4 Meaning of “achieved entropy”

Two measures are used.

**Shannon entropy** measures average uncertainty:

$$
H(X)=-\sum_xP(X=x)\log_2P(X=x).
$$

**Min-entropy** measures the probability of the easiest single guess:

$$
H_\infty(X)=-\log_2\max_xP(X=x).
$$

If $H_\infty(X)=h$, the best one-guess success probability is $2^{-h}$. For independent variables, both Shannon entropy and min-entropy add.

A deterministic checksum, encoding, hash, or key-derivation operation cannot create entropy that was absent from its input. In particular, producing a 512-bit BIP-39-derived seed does not turn a mnemonic with $h$ bits of entropy into 512 bits of security.

---

## 2. One die and one result

### 2.1 Full six-face result

For a die with probabilities $\mathbf p=(p_1,\ldots,p_6)$,

$$
H_6(\mathbf p)=-\sum_{i=1}^6p_i\log_2p_i,
\qquad
H_{\infty,6}(\mathbf p)=-\log_2\max_i p_i.
$$

For an ideal die,

$$
H_6=H_{\infty,6}=\log_2 6\approx2.5849625\text{ bits per result}.
$$

### 2.2 Binary quantization

Map faces 1, 2, 3 to zero and faces 4, 5, 6 to one. Define

$$
a=p_1+p_2+p_3,
\qquad 1-a=p_4+p_5+p_6.
$$

Then

$$
H_2(a)=-a\log_2a-(1-a)\log_2(1-a),
$$

$$
H_{\infty,2}(a)=-\log_2\max(a,1-a).
$$

An ideal die has $a=1/2$, so both measures equal one bit per result. Notice that binary quantization responds only to group bias:

- a nonuniform six-face die can still produce a perfectly uniform bit if $a=1/2$;
- a die supported only on faces 1, 2, and 3 has $a=1$ and produces zero entropy after quantization, even if those three faces are individually random.

### 2.3 Variable-length mapping

Use the mapping

$$
1\mapsto00,\quad2\mapsto01,\quad3\mapsto10,\quad4\mapsto11,
\quad5\mapsto0,\quad6\mapsto1.
$$

For an ideal die, output length is one bit with probability $1/3$ and two bits with probability $2/3$, so the expected output is $5/3$ bits per roll. Each possible one-bit output has probability $1/6$, and each possible two-bit output has probability $1/6$.

Let $P(s)$ be the probability that the generated stream begins with a fixed target string $s$, stopping as soon as its length is reached and discarding a possible extra final bit. Write $p_5$ and $p_6$ for the one-bit codeword probabilities and $p_1,\ldots,p_4$ for the two-bit codeword probabilities. Then $P(\varnothing)=1$; for one bit, $P(0)=p_5+p_1+p_2$ and $P(1)=p_6+p_3+p_4$; and for $|s|\ge2$,

$$
P(s)=p_{\rm short}(s_1)P(s_{2:})
   +p_{\rm pair}(s_1s_2)P(s_{3:}).
$$

For an ideal die this recurrence gives $P(s)=2^{-|s|}$ by induction. Thus every fixed-length output is exactly uniform, even though roll boundaries are variable. For biased dice, the same recurrence calculates each output probability; the bits must not be treated as independent without that calculation.

### 2.4 Why unrestricted “real dice” have no guarantee

The conditions $p_i\ge0$ and $\sum p_i=1$ allow

$$
\mathbf p=(1,0,0,0,0,0).
$$

Both $H_6$ and $H_{\infty,6}$ are zero, as are the entropies of the quantized bit. Repeating an independent constant result still yields a constant sequence. Therefore a numerical lower bound for real dice requires an additional bias bound, a calibrated probability model, or an unbiased-extraction procedure with explicit assumptions.

---

## 3. Multiple dice, random permutations, and batch size

### 3.1 Exact batch distribution

Let the observed ordered faces in one full batch be

$$
\mathbf x=(x_1,\ldots,x_N).
$$

Because die identities are hidden by a uniform random permutation,

$$
P(\mathbf X=\mathbf x)
=\frac{1}{N!}\sum_{\pi\in S_N}\prod_{r=1}^Np_{\pi(r),x_r}.
$$

Equivalently, the numerator is a matrix permanent. This formula—not a product of averaged face probabilities—is the exact batch distribution. Results within the observed batch are generally dependent after die identities are forgotten.

For binary quantization, replace each die's six probabilities by

$$
a_j=p_{j1}+p_{j2}+p_{j3},
\qquad 1-a_j=p_{j4}+p_{j5}+p_{j6}.
$$

For the variable-length mapping, replace each face by its one- or two-bit codeword. Because codeword boundaries depend on the observed faces, exact output probabilities for nonidentical dice must retain the die order and roll boundaries; a per-bit product model is generally invalid.

### 3.2 What random ordering can and cannot add

Let $H_j$ be the entropy of labeled die $j$. Conditioning on the permutation gives

$$
H(\mathbf X\mid\Pi)=\sum_{j=1}^NH_j.
$$

For the unlabeled observed batch,

$$
\sum_{j=1}^NH_j
\le H(\mathbf X)
\le\min\left(N\log_2 6,\ \sum_{j=1}^NH_j+\log_2N!\right).
$$

Thus hiding identities never reduces Shannon entropy relative to the labeled sequence, and its gain is at most $\log_2N!$ bits per full batch.

Writing $h_j=H_{\infty}(\mathbf p_j)$, min-entropy satisfies

$$
\sum_{j=1}^Nh_j
\le H_\infty(\mathbf X)
\le\min\left(N\log_2 6,\ \sum_{j=1}^Nh_j+\log_2N!\right).
$$

The lower bound follows because every term in the permutation mixture is at most $\prod_j\max_i p_{ji}$. The upper bound follows because at least one permutation assigns every die to one of its most likely faces.

These bounds also show why permutation is not a free guaranteed entropy source:

- if all dice have the same distribution, every permutation gives the same sequence distribution and the gain is exactly zero;
- if dice differ, the gain may be positive;
- if identities are observable to an attacker, use the labeled value $\sum H_j$ or $\sum h_j$.

### 3.3 Final partial batch

If only $t<N$ additional results are needed, the retained results are a uniformly ordered sample of $t$ distinct dice from the batch. Its exact probability is

$$
P(x_1,\ldots,x_t)
=\frac{1}{(N)_t}
\sum_{\substack{j_1,\ldots,j_t\\\text{all distinct}}}
\prod_{r=1}^tp_{j_r,x_r},
$$

where $(N)_t=N!/(N-t)!$ is the number of ordered selections. Discarding the unused dice does not justify counting their entropy.

### 3.4 Batch count

Binary quantization needs exactly $L$ retained results. Minimal fixed-length base-6 conversion needs

$$
k=\left\lceil\frac{L}{\log_2 6}\right\rceil,
$$

which is 50 digits for $L=128$ and 100 digits for $L=256$.

| Dice $N$ | Binary batches, 128 bits | Binary batches, 256 bits | Variable mapping ideal batch-equivalents, 128 bits | Variable mapping ideal batch-equivalents, 256 bits | Base-6 batches, 50 digits | Base-6 batches, 100 digits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 128 | 256 | 77.04 | 153.84 | 50 | 100 |
| 5 | 26 | 52 | 15.408 | 30.768 | 10 | 20 |
| 6 | 22 | 43 | 12.84 | 25.64 | 9 | 17 |
| 10 | 13 | 26 | 7.704 | 15.384 | 5 | 10 |
| 50 | 3 | 6 | 1.5408 | 3.0768 | 1 | 2 |

The binary and base-6 columns are fixed whole-batch counts. For the variable mapping, the exact ideal-die stopping recurrence is $E_0=0$, $E_1=1$, and $E_L=1+E_{L-1}/3+2E_{L-2}/3$. The table divides $E_L$ by $N$; rolling whole batches adds an unused partial-batch overhead. A two-bit final result can cross the target by one bit, which must be discarded. These are ergonomic quantities, not entropy improvements.

For each batch, read every die in a predetermined order and append its mapped bit or bit pair. Stop at exactly $L$ bits; if the final face produces two bits when only one position remains, retain the first bit and discard the second. Ignore all later dice in that batch without selecting them by value.

---

## 4. Converting base 6 into exactly $L$ bits

“Convert from base 6 to binary” is incomplete unless the exact mapping and rejection behavior are specified.

Let

$$
X=\sum_{r=1}^kd_r6^{k-r},\qquad d_r\in\{0,1,2,3,4,5\},
$$

so $0\le X<M=6^k$. Let $B=2^L$, $Q=\lfloor M/B\rfloor$, and $R=M-QB$.

### 4.1 Naive modulo conversion

A simple fixed-length rule is

$$
Y=X\bmod B.
$$

For ideal dice, $R$ outputs have $Q+1$ preimages and $B-R$ outputs have $Q$ preimages. Therefore

$$
H_\infty(Y)=\log_2M-\log_2(Q+1),
$$

and Shannon entropy follows by summing those two probability classes. Even ideal dice are slightly biased.

### 4.2 Range rejection

An ideal-dice rejection rule is:

1. collect $k$ base-6 digits and form $X$;
2. accept only if $X<QB$;
3. on acceptance output $Y=X\bmod B$; otherwise discard the block and restart.

For ideal dice every output has exactly $Q$ accepted preimages, so $Y$ is exactly uniform. The acceptance probability is

$$
A=\frac{QB}{M}.
$$

This simple block algorithm is analyzed here. More efficient “randomness recycling” algorithms exist but require a separate specification.

### 4.3 A critical limitation for biased dice

Range rejection corrects the mismatch between $6^k$ and $2^L$ **only when the base-6 integers are uniform**. For biased dice,

$$
P(Y=y\mid\text{accept})
=\frac{\sum_{q=0}^{Q-1}P(X=y+qB)}{P(X<QB)},
$$

which is not generally $1/B$.

Likewise, the naive rule has

$$
P(Y=y)=\sum_{\substack{q\ge0\\y+qB<M}}P(X=y+qB).
$$

Consequently, the raw base-6 entropy tables below are entropy budgets before the many-to-one conversion. They are not automatic proofs that a deterministic conversion has delivered that much seed min-entropy. Given measured $p_{ji}$ values, the displayed formulas define the exact output distribution; without such values, no universal positive guarantee exists.

A generic bound for naive conversion is useful. Since each output has at most

$$
K=\left\lceil\frac{6^k}{2^L}\right\rceil
$$

preimages,

$$
H_\infty(Y)\ge H_\infty(X)-\log_2K.
$$

This bound is conservative and may be loose. For rejection, an analogous bound also depends on the bias-dependent acceptance probability and therefore cannot be evaluated from $k$ alone.

---

## 5. Results

### 5.1 Ideal dice: exact comparison

| Target $L$ | Method | Retained dice results | Raw entropy | Output Shannon entropy | Output min-entropy | Other cost |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 128 | Binary quantization | 128 | 128 | 128 | 128 | No rejection |
| 256 | Binary quantization | 256 | 256 | 256 | 256 | No rejection |
| 128 | Variable-length mapping | About 77 rolls | 128 output bits | 128 | 128 | 77.04 expected physical rolls; possible one-bit overshoot |
| 256 | Variable-length mapping | About 154 rolls | 256 output bits | 256 | 256 | 153.84 expected physical rolls; possible one-bit overshoot |
| 128 | Base 6, naive modulo | 50 | 129.248 | 127.971 | 127.663 | Slight conversion bias |
| 256 | Base 6, naive modulo | 100 | 258.496 | 255.995 | 255.911 | Slight conversion bias |
| 128 | Base 6, rejection | 50 per attempt | 129.248 per attempt | 128 | 128 | $A=84.199\%$; 59.38 expected digits |
| 256 | Base 6, rejection | 100 per attempt | 258.496 per attempt | 256 | 256 | $A=88.618\%$; 112.84 expected digits |

For 128 bits, $Q=2$ and $K=3$. For 256 bits, $Q=5$ and $K=6$.

**Interpretation.** Binary quantization and the variable-length mapping are exactly uniform for an ideal die. The variable mapping uses every result and reduces expected rolls by 40% relative to binary, at the cost of variable completion time and a possible discarded final bit. Base 6 uses still fewer results, but naive conversion needlessly loses a small amount of entropy.

### 5.2 Illustrative model A: one heavy face

Apply the [one-heavy-face stress model](ExpectedDicePerformace.md#33-one-heavy-face-model-intuitive-stress-test) with heavy-face probability $q$, assuming the heavy face belongs to one binary group. The more likely binary value then has probability

$$
a=0.4+0.6q.
$$

Because all dice are identical and their biases are aligned, random permutation and batch size provide no entropy gain. For fixed maximum face probability $q$, equal sharing among the other faces makes Shannon entropy relatively high; it is not a universal Shannon-worst distribution.

For the variable-length mapping, let $r=(1-q)/5$. Any exact one- or two-bit codeword has probability at most $q$, while either possible first bit has probability at most $g=q+2r$. A conservative upper bound on the most likely $L$-bit output is therefore

$$
M_0=1,\qquad M_1=g,\qquad M_L=q(M_{L-1}+M_{L-2}).
$$

The corresponding min-entropy is at least $-\log_2M_L$. This bound permits the heavy face to favor every recurrence branch and can therefore be looser than the exact result for a particular face placement.

### 12-word target

Base-6 columns are the raw 50-digit entropy budget. Binary columns are the entropy of the actual 128-bit quantized sequence. The variable-mapping column is the conservative fixed-output min-entropy bound above.

| Heavy-face $q$ | Binary max $a$ | Base-6 Shannon | Base-6 min | Binary Shannon | Binary min | Variable mapping min bound |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.1667 | 0.500 | 129.248 | 129.248 | 128.000 | 128.000 | 128.000 |
| 0.1700 | 0.502 | 129.245 | 127.820 | 127.999 | 127.263 | 125.811 |
| 0.1800 | 0.508 | 129.203 | 123.697 | 127.976 | 125.069 | 119.473 |
| 0.1900 | 0.514 | 129.112 | 119.796 | 127.928 | 122.900 | 113.449 |
| 0.2000 | 0.520 | 128.974 | 116.096 | 127.852 | 120.757 | 107.709 |
| 0.2200 | 0.532 | 128.564 | 109.221 | 127.622 | 116.544 | 96.975 |
| 0.2500 | 0.550 | 127.636 | 100.000 | 127.075 | 110.400 | 82.434 |
| 0.3000 | 0.580 | 125.332 | 86.848 | 125.626 | 100.592 | 61.392 |

For a 24-word target, the base-6 and binary entries double. Re-evaluate the variable-mapping recurrence at $L=256$ rather than doubling the rounded values.

This table demonstrates why Shannon entropy alone can be reassuring while min-entropy is not. It also shows that the conservative variable-length bound can fall faster because many one- and two-bit roll paths can produce the same fixed output.

For a 12-word target to retain at least 123 raw min-entropy bits in this model (a shortfall below five bits):

- base 6 requires $q<0.18175$ before conversion;
- binary quantization requires $q<0.18954$;
- the variable-length recurrence should be evaluated for the selected threshold rather than inferred from a per-roll entropy figure.

For a 24-word target to retain at least 251 bits:

- base 6 requires $q<0.17556$ before conversion;
- binary quantization requires $q<0.17803$;
- the variable-length recurrence should be evaluated at $L=256$.

The base-6 thresholds concern the raw source; deterministic conversion can impose an additional loss.

### 5.3 Illustrative model B: bounded multiplicative bias

Apply the [bounded multiplicative model](ExpectedDicePerformace.md#31-bounded-multiplicative-bias-best-for-security-guarantees), with $0\le\varepsilon\le1$, to the conversion formulas.

The worst per-result min-entropies are

$$
H_{\infty,6}^{\rm worst}=\log_2 6-\log_2(1+\varepsilon),
$$

$$
H_{\infty,2}^{\rm worst}=1-\log_2(1+\varepsilon).
$$

For the variable-length mapping, put $u=(1+\varepsilon)/6$. Every exact codeword probability is at most $u$, and either one-bit target has at most three matching faces. Therefore

$$
M_0=1,\qquad M_1=3u,\qquad
M_L=u(M_{L-1}+M_{L-2})
$$

upper-bounds the probability of every $L$-bit output. The output min-entropy is at least $-\log_2M_L$. This is a conservative bound rather than an exact worst-case optimization: it allows every branch in the recurrence to attain $u$ simultaneously.

For Shannon entropy, a worst admissible face distribution has three faces at $(1+\varepsilon)/6$ and three at $(1-\varepsilon)/6$:

$$
H_6^{\rm worst}=\log_2 6-
\frac{(1+\varepsilon)\log_2(1+\varepsilon)
+(1-\varepsilon)\log_2(1-\varepsilon)}{2}.
$$

The same arrangement also gives the worst binary grouping, with group probabilities $(1\pm\varepsilon)/2$.

### 12-word target: conservative entropy values

| $\varepsilon$ | Base-6 Shannon, 50 digits | Base-6 min, 50 digits | Binary Shannon, 128 bits | Binary min, 128 bits | Variable mapping min bound, 128 bits |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.01 | 129.245 | 128.530 | 127.991 | 126.163 | 126.894 |
| 0.02 | 129.234 | 127.820 | 127.963 | 124.343 | 125.797 |
| 0.05 | 129.158 | 125.729 | 127.769 | 118.990 | 122.566 |
| 0.10 | 128.887 | 122.373 | 127.075 | 110.400 | 117.366 |
| 0.20 | 127.796 | 116.096 | 124.282 | 94.332 | 107.583 |

Again, the base-6 values are raw-source budgets. A value over 128 cannot produce more than a 128-bit output and does not by itself prove uniform extraction.

For practical comparison, the central scenarios defined in [Expected performance of real six-sided dice](ExpectedDicePerformace.md#4-plausible-analysis-scenarios) are $\varepsilon=0.01$ for casino-grade precision dice and $\varepsilon=0.05$ for well-made consumer dice. Under the conservative worst-alignment model, a 12-word binary sequence retains 126.163 bits in the precision scenario and 118.990 bits in the consumer scenario; the variable mapping retains at least 126.894 and 122.566 bits under its recurrence bound. All four values exceed the 112-bit conservative objective. The $\varepsilon=0.10$ row is a separate stress scenario.

### Entropy losses for both seed lengths

The following tables report loss relative to the corresponding ideal sequence. Base 6 uses 50 or 100 digits, binary uses 128 or 256 results, and the variable mapping stops after producing 128 or 256 bits.

#### 12-word entropy losses

| $\varepsilon$ | Base-6 Shannon loss | Base-6 min loss | Binary Shannon loss | Binary min loss | Variable mapping min-bound loss |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.01 | 0.004 | 0.718 | 0.009 | 1.837 | 1.106 |
| 0.02 | 0.014 | 1.428 | 0.037 | 3.657 | 2.203 |
| 0.05 | 0.090 | 3.519 | 0.231 | 9.010 | 5.434 |
| 0.10 | 0.361 | 6.875 | 0.925 | 17.600 | 10.634 |
| 0.20 | 1.452 | 13.152 | 3.718 | 33.668 | 20.417 |

#### 24-word entropy losses

| $\varepsilon$ | Base-6 Shannon loss | Base-6 min loss | Binary Shannon loss | Binary min loss | Variable mapping min-bound loss |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.01 | 0.007 | 1.436 | 0.018 | 3.675 | 2.209 |
| 0.02 | 0.029 | 2.857 | 0.074 | 7.314 | 4.399 |
| 0.05 | 0.180 | 7.039 | 0.462 | 18.020 | 10.850 |
| 0.10 | 0.723 | 13.750 | 1.850 | 35.201 | 21.236 |
| 0.20 | 2.905 | 26.303 | 7.437 | 67.337 | 40.769 |

For less than a five-bit min-entropy shortfall from the target length:

| Target | Base-6 raw-source condition | Binary condition | Variable mapping bound |
| ---: | ---: | ---: | ---: |
| 128 | $\varepsilon<0.09048$ | $\varepsilon<0.02745$ | $\varepsilon<0.04593$ |
| 256 | $\varepsilon<0.05333$ | $\varepsilon<0.01363$ | $\varepsilon<0.02276$ |

Base 6 tolerates a larger $\varepsilon$ in this raw-budget comparison because 50 ideal results contain 1.248 surplus bits and each result retains all six faces. The variable mapping's conservative bound performs between base 6 and binary here. The base-6 condition is not a universal extractor guarantee.

### 5.4 Illustrative model C: random dice from a Dirichlet distribution

Apply the [symmetric Dirichlet ensemble](ExpectedDicePerformace.md#32-symmetric-dirichlet-model-useful-for-populations-not-guarantees). The attacker is assumed to know each realized $\mathbf p_j$; uncertainty about which vector was drawn is not added as secret entropy.

The expected conditional Shannon entropies have closed forms involving the digamma function $\psi$:

$$
\mathbb E[H_6]=\frac{\psi(6\alpha+1)-\psi(\alpha+1)}{\ln2},
$$

$$
\mathbb E[H_2]=\frac{\psi(6\alpha+1)-\psi(3\alpha+1)}{\ln2}.
$$

Expected min-entropies below were estimated with 300,000 deterministic-seed Monte Carlo draws. The totals use the conservative labeled-dice benchmark, so they do not credit a possible hidden-permutation gain.

| $\alpha$ | Face-probability SD | $E[H_6]$/result | $E[H_{\infty,6}]$/result | Base $H$, 50 digits | Base $H_\infty$, 50 digits | $E[H_2]$/bit | $E[H_{\infty,2}]$/bit | Binary $H$, 128 bits | Binary $H_\infty$, 128 bits |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0.1034 | 2.3129 | 1.6121 | 115.647 | 80.607 | 0.9424 | 0.7183 | 120.625 | 91.937 |
| 10 | 0.0477 | 2.5260 | 2.0805 | 126.301 | 104.024 | 0.9881 | 0.8622 | 126.474 | 110.365 |
| 50 | 0.0215 | 2.5730 | 2.3421 | 128.649 | 117.107 | 0.9976 | 0.9360 | 127.693 | 119.802 |
| 200 | 0.0108 | 2.5820 | 2.4599 | 129.098 | 122.996 | 0.9994 | 0.9674 | 127.923 | 123.832 |

For a 24-word target, double the four total-entropy columns. Because this is an average over an ensemble, an individual die set can be better or worse. The table should not be read as a lower bound. A variable-mapping ensemble value is not reported: each realized face vector must first be evaluated with the fixed-output recurrence, then averaged using a clearly specified statistic.

### 5.5 Worked aggregate final-outcome vector

As a concrete conversion example, apply the formulas to [Labby's aggregate final-outcome vector](ExpectedDicePerformace.md#23-labbys-automated-per-face-replication). Its values, provenance, and limitations are maintained there.

| Quantity | Value |
| --- | ---: |
| Raw base-6 min-entropy for 50 results | 128.33 bits |
| Binary group probability $P(1\text{--}3)$ | 0.4999 |
| Binary min-entropy for 128 results | 127.96 bits |
| Variable-mapping output | Evaluate with the Section 2.3 recurrence |

These totals treat the supplied vector as a common independent distribution. They illustrate how the same aggregate face bias propagates differently through each conversion; they are not confidence bounds for an individual die.

### 5.6 Comparison of all four factors

| Factor | Effect on Shannon entropy | Effect on min-entropy | Security interpretation |
| --- | --- | --- | --- |
| Ideal vs real dice | Bias lowers entropy; unrestricted bias can lower it to zero | Often falls much faster than Shannon entropy | The dominant uncertainty; requires a bound, measurement, or justified extractor |
| Batch size $N$ | No change for identical dice; possible gain when hidden dice have differing biases | Same worst-case conclusion | Primarily an ergonomic factor; no guaranteed rescue from biased dice |
| Binary quantization | Keeps at most 1 bit/result; ignores within-group bias | Determined by the larger group probability | Simple; can cancel or amplify face bias depending on grouping |
| Variable-length mapping | Exactly uniform fixed-length output for ideal dice; $5/3$ expected bits per roll | Determined by all roll-boundary paths to each fixed output | Uses every face and fewer expected rolls; variable completion time |
| Base-6 conversion | Up to 2.585 raw bits/result | Sensitive to the most likely full sequence and conversion preimages | Fewer rolls, but exact conversion and bias assumptions matter |
| 12 vs 24 words | Total and loss approximately double | Total and loss approximately double | More target entropy, but a stricter dice-quality requirement for a fixed absolute loss budget |

---

## 6. Interpretation of conversion schemes

### 6.1 Which entropy measure should drive a security statement?

Use min-entropy for a conservative statement about the most likely mnemonic, and report Shannon entropy as supplementary information. The numerical examples show that Shannon losses can look negligible while min-entropy losses exceed five bits.

A statement such as “the rolls have 127.9 bits of Shannon entropy” must not be shortened to “the seed has 127.9 bits of security.”

### 6.2 Is binary quantization robust?

It is robust against biases that stay within the two groups and preserve $p_1+p_2+p_3=1/2$. It is not robust against group bias. Under the bounded multiplicative model, a 12-word binary sequence loses fewer than five min-entropy bits only when $\varepsilon<2.745\%$. The corresponding 24-word threshold for fewer than five absolute bits lost is $1.363\%$.

Changing which faces map to zero can help only if the die distribution is known and the grouping is chosen without leaking or manipulating the rolls. A fixed 3-versus-3 mapping has no universal advantage over another fixed grouping under unrestricted probabilities.

### 6.3 Is the variable-length mapping a useful compromise?

Yes. It emits bits directly, requires no base conversion, works with ordinary BIP-39 word entry after checksum completion, and uses about 40% fewer rolls than binary quantization with ideal dice. Every face contributes.

The tradeoffs are variable completion time and a more involved biased-dice analysis because several one- and two-bit roll paths can produce the same fixed output. Results must be recorded in a predetermined order, and a possible extra final bit must be discarded without changing earlier results.

### 6.4 Is base 6 better?

As a raw source, base 6 uses the roll information more efficiently and can provide more min-entropy than binary quantization for some bias models. It is not automatically safer:

- a direct modulo or truncation mapping can bias the result even for ideal dice;
- ideal-dice range rejection fixes radix mismatch but not unknown physical bias;
- a raw source entropy budget is not the same as proven entropy after a many-to-one conversion.

If base 6 is used operationally, the conversion algorithm should be fixed, reviewed, and tested against known vectors. For a quantified real-dice distribution, its exact output probabilities should be evaluated from the formulas in Section 4.

### 6.5 Does using more dice help security?

Not in the worst case. If all dice share the same distribution, $N=1$, 5, 6, 10, and 50 have the same entropy per retained result. More dice reduce the number of repeated physical throws.

If individual biases differ, invisible random ordering may increase entropy. The guaranteed gain from this fact alone is still zero because the biases could all align. It is prudent to use the labeled-dice lower benchmark unless the heterogeneity model and identity-hiding procedure have been justified.

### 6.6 Where do defensible probability inputs come from?

This document does not establish a numerical probability bound for physical dice. The empirical evidence, candidate imperfection models, and confidence-bound methodology are owned by [Expected performance of real six-sided dice](ExpectedDicePerformace.md). The requirement that a tested procedure match the generation procedure is owned by [Rolling technique and throw dynamics](RollingTechnique.md). Once a final-outcome vector or bound is supplied, the formulas above determine the consequences for each conversion scheme.

---

## 7. Worked formula checklist

For a concrete set of dice, the calculation is:

1. Supply or assume each aggregate final-outcome vector $\mathbf p_j$.
2. For base 6, calculate
   $$H_j=-\sum_ip_{ji}\log_2p_{ji},\qquad
   h_j=-\log_2\max_ip_{ji}.$$
3. For binary quantization, calculate
   $$a_j=p_{j1}+p_{j2}+p_{j3},$$
   then
   $$H_j=H_2(a_j),\qquad h_j=-\log_2\max(a_j,1-a_j).$$
4. For the variable mapping, use the Section 2.3 recurrence to calculate or bound every fixed-length output probability; do not add per-bit entropy as though the emitted bits were independent.
5. For labeled base-6 or binary results, add the entropies of every retained die result. Reuse of a die simply adds another copy because rolls are assumed independent.
6. If identities are truly hidden, use the permutation-mixture formula for an exact result or the Section 3 bounds for a conservative result.
7. For binary quantization, the resulting bit sequence has the calculated sequence entropy directly. For the variable mapping, use the recurrence result.
8. For base 6, apply the exact chosen conversion formula. Do not equate raw entropy with output entropy without analyzing the mapping.
9. Append the BIP-39 checksum. Add zero entropy for this step.

---

## 8. Limits of this analysis

- Real dice probabilities were not measured here. All nonideal numerical results depend on explicitly labeled illustrative models.
- Independence and valid aggregate final-outcome probability bounds are assumed. Correlation or model mismatch can change the result.
- The simple range-rejection method restarts whole blocks. More efficient conversion methods may consume fewer expected rolls.
- The analysis concerns randomness in the BIP-39 entropy input, not physical backup security, passphrase strength, side channels, malware, or hardware-wallet correctness.
- The Dirichlet min-entropy values are simulation estimates and not guarantees.

---

## References

- [BIP-39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- [NIST SP 800-90B: Recommendation for the Entropy Sources Used for Random Bit Generation](https://csrc.nist.gov/pubs/sp/800/90/b/final)
- Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, for Shannon entropy, conditional entropy, and entropy under mixtures.
