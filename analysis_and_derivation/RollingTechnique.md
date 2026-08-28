# Rolling technique and throw dynamics

Document navigation:

- [Overview](../README.md)
- Previous: [Expected performance of real six-sided dice](ExpectedDicePerformace.md)
- Next: [Attacker capabilities versus mnemonic entropy](AttackerCapabilties.md)

---

## Executive summary

This document owns the **rolling-method contribution** to the final-outcome distribution: container, agitation, available space, collisions, surface, settling, and reading procedure. Inherent physical-die imperfections are analyzed separately in [Expected performance of real six-sided dice](ExpectedDicePerformace.md). The conversion analysis consumes only the aggregate final-outcome probabilities produced by both contributors.

Kapitaniak et al. modeled die throws and compared the model with high-speed video. In the regimes summarized by the source review that motivated this document, a no-bounce soft landing retained strong information about the initial orientation, whereas a vigorous throw with substantial rotation and approximately four or five bounces came much closer to the fair limit. These results are evidence about a model and particular experimental regimes, not a universal certified entropy value for every hand throw.

The practical consequence is clear: **rolling technique is part of the entropy source**. The dynamics research shows a large contrast between a dead drop and a vigorous multi-collision process, so the rolling method must be specified rather than treated as an incidental detail.

The preferred practical implementation is a sufficiently large lidded shoe box or food-storage box. The original Diceware instructions recommend five dice, at least ten hard shakes, tipping the box so the dice slide to one edge, and reading them left-to-right or front-to-back. This gives the dice more room than a small cup, creates repeated wall and die collisions, contains the results, and produces an ordering without rearranging them by hand.

Only the **physical rolling workflow** is borrowed. Diceware normally interprets five d6 results as one of $6^5=7776$ passphrase words; this project applies its separate BIP-39 conversion only after the batch has been read.

---

## 1. Scope and rolling dynamics

### 1.1 Boundary with physical-die analysis

Physical geometry, mass distribution, pips, edge shape, wear, and damage are outside this document's scope. Their evidence and statistical models are maintained in the [physical-die analysis](ExpectedDicePerformace.md). This document asks how the handling process changes the distribution eventually presented to the entropy analysis.

### 1.2 Rolling dynamics

Let $S$ denote the die's initial state and release, including orientation, position, linear velocity, and angular velocity. The final distribution can be written as

$$
P(Y=i)=\sum_sP(S=s)P(Y=i\mid S=s).
$$

The rolling method affects both terms: shaking changes the distribution of starting states, while rotation and collisions change how strongly the final face depends on any one start.

Kapitaniak et al. report conditional probabilities such as

$$
P(Y=i\mid S=s).
$$

Those results demonstrate a physical mechanism by which poor technique can preserve orientation. They are deliberately conservative for this project: generation takes place in private, and an attacker able to monitor a throw closely enough to estimate its initial conditions would ordinarily also be able to read the settled secret values. The main use of the conditional analysis here is therefore to compare rolling regimes and motivate strong agitation, not to introduce a separate attacker model throughout the repository.

### 1.3 One final distribution, two contributors

A test of the complete setup—dice, container, shaking procedure, settling, and reading rule—measures their combined final distribution. This is the distribution needed by the entropy formulas. Testing the dice under a different apparatus or using a different technique during secret generation weakens that connection.

Physical-die and rolling-dynamics figures from different studies must not be multiplied, added, or reduced to their minimum as if they measured one joint setup. The [entropy analysis](DiceRollEntropyAnalysis.md) owns the formulas that map a justified aggregate final-outcome model into binary, variable-length, and base-6 entropy.

---

## 2. Evidence about throw dynamics

### 2.1 Mechanical model

Kapitaniak, Strzalko, Grabski, and Kapitaniak modeled a die as a rigid body under gravity with energy loss at table impacts. The model tracks orientation, linear velocity, angular velocity, and collision updates. High-speed video of dice released from height was used to compare simulated and observed trajectories.

The central result is not that dice are intrinsically random. For sufficiently precise initial conditions, their motion is deterministic. Apparent randomness arises because small uncertainty in initial state is amplified by rotation and repeated collisions. A symmetric shape supplies a fair limit, but a real throw approaches that limit only when its dynamics sufficiently erase the starting-state information.

### 2.2 Contrasting regimes

The source review reports the following representative results from the study's simulations:

| Regime | Reported persistence probability for the initially lowest face | Source review's conditional min-entropy interpretation |
| --- | ---: | ---: |
| No-bounce landing on a soft surface | 0.548 | 0.868 bits/result |
| Vigorous hand/cup throw, roughly 20--40 rad/s and 4--5 bounces | 0.199 | 2.329 bits/result |

These are conditional interpretations given the starting orientation, not measurements of the pooled final-face distribution produced by a shoe box or cup. The ideal single-face probability is $1/6\approx0.1667$. Their appropriate use here is comparative: low-energy drops preserve much more initial-state information than vigorous multi-bounce throws. They do not imply that every privately performed dead drop has exactly $0.868$ bits of final-outcome min-entropy, or that every vigorous roll has exactly $2.329$ bits.

These figures must not be treated as certified bounds for an arbitrary real setup. They concern a specific mechanical model, initial-condition distribution, and interpretation of orientation persistence. In particular, they do not directly provide binary or variable-mapping output entropy. They are strong evidence for specifying the procedure, not a substitute for characterizing the procedure actually used.

### 2.3 Why hard surfaces and collisions help

A soft landing dissipates translational energy immediately and may leave too little opportunity for reorientation. A harder surface allows repeated impacts. Combined with substantial initial rotation, those impacts make the final state more sensitive to small differences in the release.

The target is not a particular exact angular velocity that a user must measure. The operational proxy is vigorous agitation and repeated impacts before settling.

Dice colliding with one another can add mixing, but a crowded small cup can restrict their movement. A shoe box or similarly sized lidded food-storage box gives five or six dice substantially more travel. Repeated hard shaking creates collisions with the walls and other dice without requiring the user to estimate bounce count during an open cast.

---

## 3. Required rolling protocol

The following protocol is common to binary quantization, Oren's variable-length mapping, and base-6 recording.

### 3.1 Preferred lidded-box method

- Remove cameras, phones, smart glasses, and observers from the generation area.
- Use a clean, dry shoe box with a well-fitting lid or an opaque food-storage box of similar size.
- Prefer a sturdy container whose interior gives all dice room to travel and collide. Do not pack the box with so many dice that they cannot move freely.
- Five dice match the original Diceware procedure; six are also practical if the box remains spacious.
- Define the reading order and invalid-roll rule before any secret roll.

For each batch:

1. Put every die in the box and close the lid.
2. Shake the box vigorously for **at least ten hard shakes**, following the original Diceware recommendation. Each shake should make the dice travel and collide audibly inside the box; if crowding prevents free movement, use fewer dice or a larger box. This operationally supplies repeated collisions; one or two shakes are not treated as equivalent.
3. Put the box on a level surface and gently tip it so the dice slide toward one edge and form a readable row or shallow cluster.
4. Open the lid only after the dice have settled.
5. Read left-to-right; if some dice form a second row, use front-to-back as the predetermined tie-breaker.

This method combines agitation, containment, and ordering. Tipping after vigorous shaking is only a reading step; it must not replace the hard shakes.

### 3.2 Open-cast alternative

If no suitable lidded box is available:

1. use a large dice cup and a hard, level, clean rolling tray with a backstop;
2. reduce the batch size if the dice cannot move freely in the cup or tray;
3. shake vigorously, then cast with enough energy for visible tumbling and several impacts—approximately four or five is a useful target, not a sharp threshold;
4. never place, spin in place, gently tip, or softly drop a die as a substitute for a roll;
5. read the settled dice where they stopped using a spatial rule fixed in advance.

### 3.3 Read without selection

- Let all dice settle before reading any value.
- Do not rearrange dice by hand. Use the box-generated row or the predetermined spatial rule.
- Do not choose dice or reorder outcomes based on their values.
- Keep technique failures governed by the predefined invalid-roll rule; do not confuse them with encoding-specific rejection rules.
- A conservative simple invalid-roll rule is to discard the **entire batch** if any die leaves the intended rolling area, is cocked, or cannot be read unambiguously. Apply the rule without regard to the visible values.

### 3.4 Repeat consistently

Use the same box or cup, batch size, shaking process, settling method, and reading rule throughout generation. Procedure changes imply a different source distribution. If the intended setup was tested, secret generation should reproduce that setup rather than use a more convenient substitute.

---

## 4. Technique validation

### 4.1 Statistical boundary

The confidence intervals, sample-size calculations, and distinction between goodness-of-fit tests and probability bounds are owned by [Expected performance of real six-sided dice](ExpectedDicePerformace.md#5-testing-five-identified-dice). This section specifies only how a rolling-method test must reproduce and diagnose the physical process.

### 4.2 Scope of the test

A final-face test measures the quantity used by this project's private-generation model when the test reproduces the complete procedure. It cannot prove performance for another die set, container, batch size, or shaking method. It also cannot turn a p-value into a tight upper confidence bound; the simultaneous-interval method in the previous document is still required for a numerical $\varepsilon$ claim.

The conditional dynamics literature remains a useful diagnostic. If a procedure uses deliberate orientations, gentle drops, or repeatable trajectories, recording initial orientation during public test rolls can reveal dependence that pooling might hide. Under the preferred opaque-box method, vigorous shaking is used to randomize that state directly.

### 4.3 A technique-focused test

For nonsecret development of a rolling setup:

1. use the same dice, box or cup, batch size, number of shakes, settling method, and reading order intended for secret generation;
2. record every final face by die identity;
3. check transitions between consecutive batches and changes across time;
4. record invalid batches rather than silently deleting awkward outcomes;
5. if evaluating an open-cast method, also record approximate collision count and optionally initial orientation;
6. use video only for public test rolls and remove cameras before generating the secret.

A modest test can expose obvious defects or procedural instability. Certifying a small per-die final-face bound requires far more data than an ordinary chi-square demonstration.

---

## 5. Interface with the entropy analysis

The aggregate model passed to the entropy analysis must describe the complete final-outcome process:

- the dice and the rolling method jointly determine $p_i$;
- measurements made with strong mechanical agitation are evidence for that tested regime, not for gentle drops;
- independence must also hold at the level at which entropies are added.

A good rolling protocol does not prove a numerical bound. It makes evidence from well-agitated regimes more relevant and provides a repeatable process that can be tested. The numerical consequences of any resulting bound are maintained in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md).

Encoding choice does not repair a controlled or weakly agitated throw automatically. Proper rolling precedes the separate choice among conversion schemes.

---

## 6. Conclusions

1. Rolling technique is one contributor to the final-result distribution; inherent die imperfections are analyzed separately.
2. The dynamics evidence shows a large contrast between dead drops and vigorous multi-collision throws.
3. A spacious lidded shoe box or food-storage box, at least ten hard shakes, and a fixed left-to-right/front-to-back reading rule provide a simple established workflow.
4. A cup and open tray remain usable when the dice have enough room and make several impacts before settling.
5. Testing must reproduce the rolling process used during generation.

## References

- [orangesurf: Generating 128 bits of entropy from physical dice—a source-by-source analysis](https://gist.github.com/orangesurf/14f700323cb760d275d898418f6d8eab)
- M. Kapitaniak, J. Strzalko, J. Grabski, and T. Kapitaniak, [“The three-dimensional dynamics of the die throw”](https://doi.org/10.1063/1.4746038), *Chaos* 22, 047504, 2012.
- [Arnold G. Reinhold: The Diceware Passphrase Home Page](https://theworld.com/~reinhold/diceware.html)
