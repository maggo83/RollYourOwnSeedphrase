# Expected performance of real six-sided dice

Document navigation:

- [Overview](README.md)
- Previous: [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md)
- Next: [Attacker capabilities versus mnemonic entropy](AttackerCapabilties.md)

---

## Executive summary

Public evidence that maps a commercial die category directly to six measured face probabilities is sparse. Precision casino dice have much tighter geometric manufacturing tolerances than ordinary consumer dice, but a dimensional tolerance does not by itself establish a probability bound. Published roll experiments provide some evidence that ordinary dice can perform close to ideal under suitable throwing conditions, but the available studies do not justify a universal value of the bias parameter $\varepsilon$ for all casino, board-game, or role-playing dice.

For security analysis, the most useful model is therefore a **bounded multiplicative bias**:

$$
\frac{1-\varepsilon}{6}\le p_i\le\frac{1+\varepsilon}{6}
$$

for every face of every die. This model is auditable and produces conservative entropy bounds. Values such as $\varepsilon=0.005$, $0.01$, or $0.02$ for casino dice and $0.02$, $0.05$, or $0.10$ for consumer dice are useful **scenarios**, not empirically certified product specifications.

A defensible claim about a particular set of dice requires either a manufacturer-supplied probabilistic guarantee or a roll test with simultaneous confidence bounds. Testing small bias rigorously is expensive: for five identifiable dice, approximately 80,000 joint cup throws are a reasonable planning figure for having a high chance to certify $\varepsilon<0.05$ when the dice are genuinely close to ideal.

---

## 1. Definition of die bias

For die $j$, let

$$
\mathbf p_j=(p_{j1},\ldots,p_{j6}),
\qquad \sum_{i=1}^6p_{ji}=1.
$$

Define its multiplicative deviation from ideal as

$$
\varepsilon_j=\max_{i=1,\ldots,6}|6p_{ji}-1|.
$$

For a set of $D$ dice, define

$$
\varepsilon_{\max}=\max_{j=1,\ldots,D}\varepsilon_j.
$$

The statement $\varepsilon_{\max}\le\varepsilon$ is equivalent to

$$
\frac{1-\varepsilon}{6}\le p_{ji}\le\frac{1+\varepsilon}{6}
$$

for every die and face.

| $\varepsilon$ | Permitted probability of each face |
| ---: | ---: |
| 0.005 | 0.16583–0.16750 |
| 0.01 | 0.16500–0.16833 |
| 0.02 | 0.16333–0.17000 |
| 0.05 | 0.15833–0.17500 |
| 0.10 | 0.15000–0.18333 |
| 0.20 | 0.13333–0.20000 |

This is a statement about long-run roll probabilities under a specified rolling procedure. It is not merely a statement about dimensions, center of mass, or appearance.

---

## 2. Evidence found

### 2.1 Manufacturing descriptions

*Encyclopaedia Britannica* distinguishes sharp-edged casino dice from round-cornered machine-made consumer dice and reports that casino dice are commonly true to a dimensional tolerance of $0.0001$ inch. Casino supplier TCSJOHNHUXLEY describes its dice as precision products manufactured for regulated gaming environments.

These sources support the qualitative conclusion that casino dice receive substantially tighter manufacturing control. They do **not** publish corresponding bounds on the six values $p_i$.

The missing conversion is important:

$$
\text{geometric tolerance}\not\Rightarrow\text{known probability tolerance}.
$$

Roll probabilities also depend on:

- density and center-of-mass uniformity;
- pip excavation and filling;
- edge and corner geometry;
- wear and surface damage;
- cup, surface, release height, and collision dynamics;
- correlations or controlled throws.

### 2.2 Large historical roll experiment

Iversen, Longcor, Mosteller, Gilbert, and Youtz published “Bias and Runs in Dice Throwing and Recording: A Few Million Throws” in *Psychometrika* in 1971. The reported experiment used:

- 219 dice;
- four brands;
- 20,000 throws per die;
- 4,380,000 throws in total;
- recorded even/odd outcomes rather than all six faces.

The abstract reports that results were generally close to theoretical expectations. A two-million-bit set from one brand did not show a significant aggregate departure from ideal location or scale.

This is meaningful evidence that physical dice can generate sequences close to an ideal binary model. It does not establish a modern product-class value of $\varepsilon$ because:

- the experiment is from 1971;
- only even/odd grouping was recorded;
- aggregate agreement can hide individual face biases that cancel;
- “not statistically significant” is not an upper confidence bound of a chosen size;
- the relationship between those brands and current casino or consumer dice is unclear.

With 20,000 binary observations from one die, the ordinary standard error near probability $1/2$ is

$$
\sqrt{\frac{0.5(1-0.5)}{20{,}000}}\approx0.00354.
$$

Even that substantial experiment cannot resolve extremely small binary biases for each individual die with high confidence.

### 2.3 Bevelled versus sharp-edged dice

The preprint “How the Dice Fall: Investigating the Final State Probabilities of Bevelled Versus Non-bevelled Dice” reports greater final-state probability variation for bevelled dice than non-bevelled dice. It supports the physical intuition that edge geometry matters.

Its evidential weight is limited because it is a preprint rather than an established product survey, and its particular dice and experimental setup do not define universal performance bounds for commercial categories.

### 2.4 Evidence assessment

| Evidence | What it supports | What it does not support |
| --- | --- | --- |
| Casino dimensional tolerances | Casino dice are manufactured much more precisely | A numerical bound on $p_i$ or $\varepsilon$ |
| Casino supplier statements | Precision and consistency are explicit design goals | Independent probabilistic certification |
| 1971 multi-million-throw experiment | Dice can produce near-ideal binary sequences | Modern six-face bounds by product class |
| Bevelled/non-bevelled preprint | Geometry can influence final-state variation | A universal consumer-die bias distribution |

The central evidence gap is a modern, independent dataset containing many identified dice from known product classes, a controlled but realistic cup-throw protocol, all six face outcomes, and enough repetitions per die to produce narrow simultaneous confidence intervals.

---

## 3. Which imperfection model is most appropriate?

### 3.1 Bounded multiplicative bias: best for security guarantees

The $\varepsilon$ model is the most relevant model for conservative entropy analysis because it answers a direct question:

> If no face of any die deviates from ideal by more than a specified relative amount, what entropy is guaranteed?

It does not claim to describe how defects arise. Its usefulness depends on whether testing or a credible specification can justify the bound.

### 3.2 Symmetric Dirichlet model: useful for populations, not guarantees

A symmetric model

$$
\mathbf p_j\sim\operatorname{Dirichlet}(\alpha,\ldots,\alpha)
$$

represents independent dice whose biases vary randomly and symmetrically around $1/6$. Its face-probability relative standard deviation is

$$
\frac{\sigma_p}{1/6}=\sqrt{\frac{5}{6\alpha+1}}.
$$

| Assumed relative SD of a face probability | Corresponding $\alpha$ |
| ---: | ---: |
| 1% | approximately 8,333 |
| 2% | approximately 2,083 |
| 5% | approximately 333 |
| 10% | approximately 83 |
| 20% | approximately 20.7 |

The model is mathematically convenient but not strongly physical. Real defects may create correlations across opposite faces or geometric axes. A Dirichlet average also cannot provide a worst-case guarantee for a particular die.

### 3.3 One-heavy-face model: intuitive stress test

The model

$$
\left(q,\frac{1-q}{5},\ldots,\frac{1-q}{5}\right)
$$

is easy to understand, and its smallest containing multiplicative bound is

$$
\varepsilon=6q-1.
$$

It is not a realistic universal defect pattern: a physical imperfection need not make exactly one face heavy or distribute the deficit equally across five faces. It is best retained as an illustrative stress test.

### 3.4 A more realistic research model

If sufficient data existed, a hierarchical logistic-normal or structured multinomial model would be preferable. It could represent:

- systematic product-level effects;
- variation from die to die;
- correlations between opposite faces;
- effects of edge geometry and center of mass;
- rolling-procedure and surface effects.

For security certification, such a descriptive model should still be converted into a conservative per-die upper bound or a lower confidence bound on min-entropy.

---

## 4. Plausible analysis scenarios

The following ranges are **sensitivity-analysis choices**, not measured guarantees.

| Product scenario | Optimistic | Central illustrative case | Stress case |
| --- | ---: | ---: | ---: |
| New casino-grade precision dice | $\varepsilon=0.005$ | $\varepsilon=0.01$ | $\varepsilon=0.02$ |
| Good branded consumer dice | $\varepsilon=0.02$ | $\varepsilon=0.05$ | $\varepsilon=0.10$ |
| Cheap, decorative, damaged, or visibly irregular dice | $\varepsilon=0.10$ | $\varepsilon=0.20$ | higher or unrestricted |

These values are reasonable for asking “what if?” They must not be phrased as “casino dice satisfy $\varepsilon=0.01$” or “ordinary dice satisfy $\varepsilon=0.05$” without supporting measurements.

For the one-heavy-face model, the corresponding heavy probability is

$$
q=\frac{1+\varepsilon}{6}.
$$

| $\varepsilon$ | One-heavy $q$ |
| ---: | ---: |
| 0.01 | 0.16833 |
| 0.02 | 0.17000 |
| 0.05 | 0.17500 |
| 0.10 | 0.18333 |
| 0.20 | 0.20000 |

---

## 5. Testing five identified dice

### 5.1 Simultaneous 95% confidence bound

Suppose five identifiable dice are thrown together $n$ times and every face is recorded separately. Each die then has $n$ observations. There are 30 die-face probabilities to bound simultaneously.

For die $j$ and face $i$, let $X_{ji}$ be its observed count. A rigorous procedure is:

1. construct binomial Clopper–Pearson intervals for every $p_{ji}$;
2. Bonferroni-adjust the intervals so all 30 cover simultaneously with at least 95% confidence;
3. calculate
   $$
   \varepsilon_U=
   \max_{j,i}\max\left(|6L_{ji}-1|,|6U_{ji}-1|\right).
   $$

Then $\varepsilon_U$ is a simultaneous 95% upper confidence bound for $\varepsilon_{\max}$.

Near ideal probabilities, the approximate uncertainty margin expressed in $\varepsilon$ units is

$$
r_\varepsilon\approx\frac{7.03}{\sqrt n}.
$$

The constant $7.03$ uses a normal approximation with Bonferroni simultaneous coverage over $5\times6=30$ proportions at an overall 95% confidence level. The final analysis should use the exact intervals; this approximation is for planning sample size.

| Desired confidence-bound margin | Joint cup throws | Total die outcomes |
| ---: | ---: | ---: |
| 0.10 | about 4,950 | 24,750 |
| 0.05 | about 19,800 | 99,000 |
| 0.03 | about 55,000 | 275,000 |
| 0.02 | about 123,600 | 618,000 |
| 0.01 | about 494,000 | 2,470,000 |

The final bound is approximately

$$
\varepsilon_U\approx\widehat\varepsilon_{\max}+r_\varepsilon,
$$

so interval precision is not the same as proving that $\varepsilon$ lies below that margin.

### 5.2 Certifying $\varepsilon<0.05$

Use the hypotheses

$$
H_0:\varepsilon_{\max}\ge0.05,
\qquad
H_1:\varepsilon_{\max}<0.05.
$$

Certify the dice only if the simultaneous upper bound satisfies

$$
\varepsilon_U<0.05.
$$

This controls false certification at no more than 5%. The number of throws needed to pass with high probability depends on how far the true bias lies below $0.05$. A conservative approximate design is

$$
n\approx4\left(\frac{7.03}{0.05-\varepsilon_0}\right)^2,
$$

where $\varepsilon_0$ is the largest true bias for which approximately 95% passing probability is desired.

| Assumed true $\varepsilon_{\max}$ | Approximate joint throws for 95% passing probability |
| ---: | ---: |
| 0.00 | 79,100 |
| 0.01 | 123,600 |
| 0.02 | 219,700 |
| 0.03 | 494,200 |
| 0.04 | 1,977,000 |
| approaching 0.05 | approaches infinity |

No finite experiment can reliably distinguish $0.049999$ from $0.050001$. An indifference gap is unavoidable.

### 5.3 Operational test requirements

A test should reproduce the intended entropy-generation process:

- use the same dice, cup, surface, release method, and approximate height;
- track every die separately during testing;
- predefine the sample size or use a valid sequential-testing design;
- check serial dependence and changes over time, not only face counts;
- do not reuse secret-generation outcomes as public test data;
- retest after damage, substantial wear, or a changed procedure.

Passing a chi-square test is not equivalent to obtaining a useful upper bound on $\varepsilon$.

---

## 6. Entropy relevance

For binary quantization of 128 retained results, the bounded model gives

$$
H_\infty\ge128\left[1-\log_2(1+\varepsilon)\right].
$$

Base-4 rejection accepts faces 1–4 as 00, 01, 10, and 11 and discards faces 5–6. If

$$
A=p_1+p_2+p_3+p_4,
$$

then accepted face $i$ has conditional probability $p_i/A$. Under the bounded multiplicative model,

$$
\frac{2-\varepsilon}{3}\le A\le\frac{2+\varepsilon}{3}
$$

and

$$
H_{\infty,4}\ge
\log_2\frac{4-2\varepsilon}{1+\varepsilon}
$$

bits per accepted two-bit symbol.

| $\varepsilon$ | Binary, 12 words | Base 4, 12 words | Binary, 24 words | Base 4, 24 words |
| ---: | ---: | ---: | ---: | ---: |
| 0.01 | 126.16 bits | 126.62 bits | 252.33 bits | 253.24 bits |
| 0.02 | 124.34 bits | 125.24 bits | 248.69 bits | 250.49 bits |
| 0.05 | 118.99 bits | 121.16 bits | 237.98 bits | 242.32 bits |
| 0.10 | 110.40 bits | 114.46 bits | 220.80 bits | 228.93 bits |
| 0.20 | 94.33 bits | 101.44 bits | 188.66 bits | 202.88 bits |

Thus a defensible $\varepsilon\le0.05$ bound leaves approximately 119 bits with binary quantization or 121 bits with base-4 rejection for 12 words. Operational compromise is then much more plausible than classical brute force. Base-4 rejection does not remove physical bias: it conditions the distribution on faces 1–4.

Roll the full batch, read dice in a predetermined order, retain only faces 1–4, and then roll the full batch again. Continue until exactly 64 or 128 accepted symbols have been recorded. In the final batch, keep accepted symbols in the predetermined order only until the target is reached; ignore every later die.

For ideal dice, the expected accepted symbols per batch are $2N/3$:

| Dice per batch | Expected accepted symbols | Batch-equivalents, 12 words | Batch-equivalents, 24 words |
| ---: | ---: | ---: | ---: |
| 1 | 0.67 | 96.0 | 192.0 |
| 5 | 3.33 | 19.2 | 38.4 |
| 6 | 4.00 | 16.0 | 32.0 |

These are expected physical-roll counts divided by the batch size, not exact expected whole-batch counts. A whole final batch creates a small unused-results overhead. At $\varepsilon=0.10$, the corresponding worst-case batch-equivalents are approximately 20.21 and 40.42 with five dice, or 16.84 and 33.68 with six dice. Actual completion time is random.

---

## 7. Conclusions

1. Casino dice are physically more precise than ordinary dice, but available dimensional specifications do not establish numerical probability bounds.
2. Existing roll studies support “often close to ideal,” not a universal $\varepsilon$ for a product category.
3. The bounded multiplicative model is the correct primary model for conservative security analysis.
4. Dirichlet and one-heavy-face models are useful illustrations, not security guarantees.
5. Scenario values should remain explicitly hypothetical until supported by per-die measurements.
6. Certifying small bias is data-intensive; testing methodology and independence matter as much as the number of throws.
7. Base-4 rejection is a practical intermediate method: simple binary output, fewer expected rolls than binary quantization, and no large-integer conversion, but rejected outcomes contribute no entropy and bias among accepted faces remains.

## References

- [Encyclopaedia Britannica: Dice](https://www.britannica.com/topic/dice)
- [TCSJOHNHUXLEY: Precision Casino Dice](https://tcsjohnhuxley.com/product/precision-casino-dice/)
- G. R. Iversen, W. H. Longcor, F. Mosteller, J. P. Gilbert, and C. Youtz, [“Bias and Runs in Dice Throwing and Recording: A Few Million Throws”](https://doi.org/10.1007/BF02291418), *Psychometrika* 36, 1971, pp. 1–19.
- D. N. Loria, [“How the Dice Fall: Investigating the Final State Probabilities of Bevelled Versus Non-bevelled Dice”](https://doi.org/10.21203/rs.3.rs-2069818/v1), preprint.
- [NIST SP 800-90B: Recommendation for the Entropy Sources Used for Random Bit Generation](https://csrc.nist.gov/pubs/sp/800/90/b/final)
