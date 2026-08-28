# Expected performance of real six-sided dice

Document navigation:

- [Overview](../README.md)
- Previous: [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md)
- Next: [Rolling technique and throw dynamics](RollingTechnique.md)

---

## Executive summary

Public evidence that maps a commercial die category directly to six measured face probabilities is sparse. Precision casino dice have much tighter geometric manufacturing tolerances than ordinary consumer dice, but a dimensional tolerance does not by itself establish a probability bound. Weldon's historical data, Labby's automated replication, and a multi-million-throw binary experiment show that ordinary dice can perform close to ideal under suitable agitation. In Labby's aggregate d6 data, the largest deviation corresponds to approximately $\varepsilon=0.013$, making $\varepsilon=0.02$ a useful evidence-anchored sensitivity case for that setup. This is stronger evidence than a purely hypothetical scenario, but it is not a universal product-class guarantee.

For security analysis, the most useful model is therefore a **bounded multiplicative bias**:

$$
\frac{1-\varepsilon}{6}\le p_i\le\frac{1+\varepsilon}{6}
$$

for every face of every die. This model is auditable and produces conservative entropy bounds. Values such as $\varepsilon=0.005$, $0.01$, or $0.02$ for casino dice and $0.02$, $0.05$, or $0.10$ for consumer dice are useful **scenarios**, not empirically certified product specifications.

A defensible claim about a particular set of dice and rolling procedure requires either a manufacturer-supplied probabilistic guarantee or a roll test with simultaneous confidence bounds. Testing small bias rigorously is expensive: for five identifiable dice, approximately 80,000 joint throws are a reasonable planning figure for having a high chance to certify $\varepsilon<0.05$ when the complete setup is genuinely close to ideal. The next document explains why the rolling procedure used for testing and generation must match.

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

## 2. Evidence about marginal face bias

### 2.1 Manufacturing descriptions

*Encyclopaedia Britannica* distinguishes sharp-edged casino dice from round-cornered machine-made consumer dice and reports that casino dice are commonly true to a dimensional tolerance of $0.0001$ inch. Casino supplier TCSJOHNHUXLEY describes its dice as precision products manufactured for regulated gaming environments.

These sources support the qualitative conclusion that casino dice receive substantially tighter manufacturing control. They do **not** publish corresponding bounds on the six values $p_i$.

The missing conversion is important:

$$
\text{geometric tolerance}\not\Rightarrow\text{known probability tolerance}.
$$

Physical-die probabilities can be affected by:

- density and center-of-mass uniformity;
- pip excavation and filling;
- edge and corner geometry;
- wear and surface damage.

The rolling process is a separate contributor to the observed final distribution and is analyzed in [Rolling technique and throw dynamics](RollingTechnique.md).

### 2.2 Weldon and Pearson

W. F. R. Weldon reported 26,306 casts of twelve dice, giving 315,672 individual results. Only the number of 5-or-6 outcomes per cast was recorded. The combined observed probability was

$$
P(5\text{ or }6)=\frac{106{,}602}{315{,}672}\approx0.3377,
$$

slightly above the fair value $1/3$. Pearson's original chi-square analysis rejected the fair-binomial model; later reanalysis continued to support a small stable aggregate bias.

The experiment does not identify the separate probabilities of faces 5 and 6. Consequently, a single-face maximum such as $0.1710$ can be obtained only by adding an allocation assumption about the excess; it is not a distribution-free bound from Weldon's recorded statistic. The study establishes modest aggregate bias in that setup, not a full six-face entropy estimate.

### 2.3 Labby's automated per-face replication

Labby automated Weldon's experiment with twelve inexpensive rounded plastic dice on a mechanically agitated platform. The experiment again produced 26,306 casts and 315,672 individual outcomes, this time recording every face:

| Face | Aggregate probability |
| ---: | ---: |
| 1 | 0.1686 |
| 2 | 0.1651 |
| 3 | 0.1662 |
| 4 | 0.1658 |
| 5 | 0.1655 |
| 6 | 0.1688 |

The aggregate distribution is measurably nonuniform but close to ideal. Its maximum point estimate gives

$$
H_{\infty,6}=-\log_2(0.1688)\approx2.567
$$

raw bits per result, compared with the ideal $2.585$. The high-face probability corresponds to approximately $\varepsilon=0.013$ as a point estimate. It is not a simultaneous bound for every face of every die, and raw six-face min-entropy does not determine binary-group or variable-mapping output entropy by itself.

Labby measured the 1--6 axis as approximately $0.2\%$ shorter than the other axes, consistent with the two largest faces being favored by a small shape error. The cast sequence's reported autocorrelation and spectrum showed no evident serial structure under the machine's strong agitation. This is useful evidence about that set and apparatus, not a product-class guarantee or a study of a low-energy hand drop.

The combined 5-or-6 probability was approximately $0.3343$, close to the fair value $1/3$; the automated replication therefore did not reproduce Weldon's particular 5-or-6 excess. Its detectable pattern was instead the small 1-and-6 elevation associated with the shorter axis.

The smallest bounded-multiplicative model containing the aggregate point estimates has $\widehat\varepsilon=0.0128$. This is the empirical output this document passes to the conversion analysis. The method-specific entropy consequences are calculated once in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md#55-worked-aggregate-final-outcome-vector).

### 2.4 Large binary roll experiment

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

### 2.5 Bevelled versus sharp-edged dice

The preprint “How the Dice Fall: Investigating the Final State Probabilities of Bevelled Versus Non-bevelled Dice” reports greater final-state probability variation for bevelled dice than non-bevelled dice. It supports the physical intuition that edge geometry matters.

Its evidential weight is limited because it is a preprint rather than an established product survey, and its particular dice and experimental setup do not define universal performance bounds for commercial categories.

### 2.6 Evidence assessment

| Evidence | What it supports | What it does not support |
| --- | --- | --- |
| Casino dimensional tolerances | Casino dice are manufactured much more precisely | A numerical bound on $p_i$ or $\varepsilon$ |
| Casino supplier statements | Precision and consistency are explicit design goals | Independent probabilistic certification |
| Weldon/Pearson 5-or-6 counts | Small stable aggregate bias can occur | A separate probability for every face |
| Labby automated per-face counts | Cheap dice can be close to ideal under strong mechanical agitation | A per-die or product-class bound; performance under another rolling procedure |
| 1971 multi-million-throw experiment | Dice can produce near-ideal binary sequences | Modern six-face bounds by product class |
| Bevelled/non-bevelled preprint | Geometry can influence final-state variation | A universal consumer-die bias distribution |

The central evidence gap is a modern, independent dataset containing many identified dice from known product classes, a controlled but realistic box- or cup-rolling protocol, all six final-face outcomes, and enough repetitions per die to produce narrow simultaneous confidence intervals.

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

These values are reasonable for asking “what if?” They must not be phrased as “casino dice satisfy $\varepsilon=0.01$” or “ordinary dice satisfy $\varepsilon=0.05$” without supporting measurements. Labby's aggregate point estimate falls between the $\varepsilon=0.01$ and $0.02$ scenarios. It gives the $0.02$ consumer scenario a concrete empirical anchor under strong mechanical agitation, while $0.05$ and $0.10$ remain progressively conservative stress cases. One tested set under one machine cannot convert any of them into a general guarantee.

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

| Desired confidence-bound margin | Joint rolling batches | Total die outcomes |
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

### 5.3 Statistical test requirements

- Track every die separately during testing.
- Predefine the sample size or use a valid sequential-testing design.
- Use simultaneous confidence bounds rather than treating a nonsignificant goodness-of-fit test as proof of fairness.
- Check serial dependence and changes over time, not only face counts.
- Retest after damage or substantial wear.

This section owns the statistical inference. The process-control requirement—using the same container, batch size, agitation, settling method, and reading rule during testing and generation—is specified in [Rolling technique and throw dynamics](RollingTechnique.md#34-repeat-consistently).

---

## 6. Handoff to the conversion analysis

This document produces evidence-based or hypothetical inputs such as a full face-probability vector, a per-die upper confidence bound, or a scenario value of $\varepsilon$. It does not own the entropy formulas for binary, variable-length, or base-6 conversion. Those consequences—including the canonical tables—are calculated in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md#5-results).

---

## 7. Conclusions

1. Casino dice are physically more precise than ordinary dice, but available dimensional specifications do not establish numerical probability bounds.
2. Weldon, Labby, and Iversen support “often close to ideal under suitable agitation,” not a universal $\varepsilon$ for a product category.
3. Labby's aggregate point estimate is an empirical benchmark, not a simultaneous per-die guarantee.
4. The bounded multiplicative model is the correct primary model for conservative marginal-bias analysis.
5. Dirichlet and one-heavy-face models are useful illustrations, not security guarantees.
6. Scenario values should remain explicitly hypothetical until supported by per-die measurements.
7. Certifying small bias is data-intensive, and the tested rolling procedure must match the generation procedure.
8. Conversion-method consequences are derived in the entropy analysis and synthesized into recommendations in [Practical implications](PracticalImplications.md).

## References

- [Encyclopaedia Britannica: Dice](https://www.britannica.com/topic/dice)
- [TCSJOHNHUXLEY: Precision Casino Dice](https://tcsjohnhuxley.com/product/precision-casino-dice/)
- Karl Pearson, [“On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling”](https://doi.org/10.1080/14786440009463897), *Philosophical Magazine* 50(302), 1900, pp. 157–175.
- Zacariah Labby, [“Weldon's Dice, Automated”](https://doi.org/10.1080/09332480.2009.10722977), *CHANCE* 22(4), 2009, pp. 6–13.
- G. R. Iversen, W. H. Longcor, F. Mosteller, J. P. Gilbert, and C. Youtz, [“Bias and Runs in Dice Throwing and Recording: A Few Million Throws”](https://doi.org/10.1007/BF02291418), *Psychometrika* 36, 1971, pp. 1–19.
- D. N. Loria, [“How the Dice Fall: Investigating the Final State Probabilities of Bevelled Versus Non-bevelled Dice”](https://doi.org/10.21203/rs.3.rs-2069818/v1), preprint.
- [orangesurf: Generating 128 bits of entropy from physical dice—a source-by-source analysis](https://gist.github.com/orangesurf/14f700323cb760d275d898418f6d8eab)
- [NIST SP 800-90B: Recommendation for the Entropy Sources Used for Random Bit Generation](https://csrc.nist.gov/pubs/sp/800/90/b/final)
