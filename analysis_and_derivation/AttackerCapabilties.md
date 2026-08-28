# Attacker capabilities versus mnemonic entropy

Document navigation:

- [Overview](../README.md)
- Previous: [Rolling technique and throw dynamics](RollingTechnique.md)
- Next: [Practical implications](PracticalImplications.md)

---

## Executive summary

A properly generated 12-word BIP-39 mnemonic has 128 independent entropy bits. No publicly demonstrated classical attacker—including a nation-state—can exhaust that space. Recent public reporting on cryptocurrency theft by sophisticated actors such as the Lazarus Group emphasizes social engineering, malware, compromised software, exchange intrusion, and theft of keys or seed phrases, not brute force of uniformly generated 128-bit secrets.

The relevant security quantity is **min-entropy**. As a practical scale:

- below 50 bits is unsafe against ordinary attackers;
- 50–64 bits can enter organized GPU territory;
- 64–80 bits is not a comfortable cryptographic security level despite being difficult today;
- 96 bits is beyond realistic current brute force but below conservative long-term standards;
- 112 bits is an established conservative security strength;
- 128 bits is the appropriate target and matches Bitcoin's approximate classical elliptic-curve security level.

A 12-word dice sequence whose final outcomes satisfy the bounded model with $\varepsilon\le0.05$ has at least approximately 119 bits of min-entropy with binary quantization or 122.6 bits under the conservative Oren's variable-length mapping recurrence. The bound must describe the actual dice-and-rolling process. Under that assumption, both remain beyond plausible classical brute force; operational compromise becomes the dominant threat.

---

## 1. Scope and assumptions

This document analyzes an offline attacker who:

- knows a target address or other efficient candidate-verification condition;
- knows the generation procedure and source distribution;
- guesses candidates in optimal probability order;
- cannot observe or steal the original secret directly.

The attacker is nevertheless assumed to know the generation method and its final-outcome probability model. Direct observation of the private generation process is outside this offline brute-force model because it can reveal the results themselves; it is listed below as an operational compromise.

This is intentionally favorable to the attacker. It does not model vulnerabilities in wallet software, hardware, backups, passphrases, or user behavior.

If the mnemonic distribution has min-entropy $h$, its most likely value has probability at most

$$
2^{-h}.
$$

After $G$ optimal guesses, a conservative generic success bound is

$$
P_{\rm success}\le\min\left(1,\frac{G}{2^h}\right).
$$

For a uniform space, expected discovery occurs after approximately $2^{h-1}$ guesses.

---

## 2. Why attack rates are scenarios, not measurements

A “seed guess” is not a single inexpensive hash. Depending on the target and implementation, verification can require:

- BIP-39 PBKDF2-HMAC-SHA512 with 2,048 iterations;
- BIP-32 hierarchical key derivation;
- secp256k1 public-key operations;
- address generation and comparison;
- multiple derivation paths or address types if those are unknown.

Published hardware benchmarks for isolated hashes therefore cannot be copied directly into a complete wallet-guess rate. The following rates are deliberately broad sensitivity scenarios for **complete verified candidates per second**:

| Threat scenario | Illustrative complete-candidate rate |
| --- | ---: |
| Hobbyist CPU or simple script | $10^4$–$10^6$/s |
| One or several GPUs | $10^6$–$10^8$/s |
| Well-funded criminal cluster | $10^9$–$10^{11}$/s |
| Extreme state-scale planning scenario | $10^{12}$/s |
| Deliberately implausible future stress scenario | $10^{15}$/s |

The upper rows should not be read as observed Lazarus Group benchmarks. In many real BIP-39 attacks they overstate attainable rates, which is appropriate for conservative planning.

---

## 3. Searchable entropy by time and rate

An attacker making $R$ guesses per second performs

$$
G=RT
$$

guesses in time $T$. The size of the exhaustible space is

$$
h_{\rm exhaust}=\log_2(RT).
$$

| Rate | One year | Ten years | One hundred years |
| ---: | ---: | ---: | ---: |
| $10^6$/s | 44.8 bits | 48.2 bits | 51.5 bits |
| $10^9$/s | 54.8 bits | 58.1 bits | 61.5 bits |
| $10^{12}$/s | 64.8 bits | 68.1 bits | 71.4 bits |
| $10^{15}$/s | 74.7 bits | 78.1 bits | 81.4 bits |

Exhaustion is not an adequate safety criterion. A strong design should make even partial-search success negligible.

### 3.1 Negligible-success criterion

Requiring at most

$$
P_{\rm success}=2^{-32}\approx2.3\times10^{-10}
$$

over a 100-year attack gives

$$
h\ge\log_2(RT)+32.
$$

| Assumed complete-candidate rate | Required entropy for $P_{\rm success}\le2^{-32}$ over 100 years |
| ---: | ---: |
| $10^6$/s | approximately 84 bits |
| $10^9$/s | approximately 94 bits |
| $10^{12}$/s | approximately 104 bits |
| $10^{15}$/s | approximately 114 bits |

This illustrates why 112–128 bits is a reasonable target even though approximately 80 bits is likely beyond practical present-day exhaustive search.

---

## 4. Expected search times

For a uniform $h$-bit source,

$$
T_{\rm expected}=\frac{2^{h-1}}R.
$$

| Min-entropy | $10^6$/s | $10^9$/s | $10^{12}$/s | $10^{15}$/s |
| ---: | ---: | ---: | ---: | ---: |
| 40 bits | 6.4 days | 9.2 minutes | 0.55 seconds | negligible |
| 50 bits | 17.8 years | 6.5 days | 9.4 minutes | 0.56 seconds |
| 60 bits | 18,300 years | 18.3 years | 6.7 days | 9.6 minutes |
| 70 bits | 18.7 million years | 18,700 years | 18.7 years | 6.8 days |
| 80 bits | 19.2 billion years | 19.2 million years | 19,200 years | 19.2 years |
| 90 bits | $1.96\times10^{13}$ years | 19.6 billion years | 19.6 million years | 19,600 years |
| 100 bits | $2.0\times10^{16}$ years | $2.0\times10^{13}$ years | 20 billion years | 20 million years |
| 112 bits | $8.2\times10^{19}$ years | $8.2\times10^{16}$ years | $8.2\times10^{13}$ years | 82 billion years |
| 128 bits | $5.4\times10^{24}$ years | $5.4\times10^{21}$ years | $5.4\times10^{18}$ years | $5.4\times10^{15}$ years |

Even the $10^{15}$/s column is a stress scenario far beyond a plausible present complete BIP-39 cracking rate.

---

## 5. Threat-actor interpretation

Actor labels are imprecise. Hardware access, software quality, target value, parallelism, electricity, and time horizon vary widely. The following is a risk classification, not an attribution of measured capacity.

| Achieved min-entropy | Approximate assessment |
| ---: | --- |
| 32–40 bits | Trivial or easy once offline verification is possible |
| 40–50 bits | CPU or small-GPU territory |
| 50–60 bits | Organized GPU budget |
| 60–70 bits | Very large cluster or extreme state-scale concern |
| 70–80 bits | Extreme present/future classical assumptions |
| 80–96 bits | Not realistically brute-forceable today, but below conservative standards |
| 96–112 bits | Very strong; increasing long-term margin up to established standards |
| 112–128 bits | Conservative long-term classical security |
| 128 bits | Full 12-word BIP-39 entropy target |

Recommended minima by threat model are:

| Threat model | Minimum comfortable min-entropy | Preferred target |
| --- | ---: | ---: |
| Casual CPU attacker | 64 bits | 80+ bits |
| Criminal GPU operation | 80 bits | 96+ bits |
| Highly funded organized attacker | 96 bits | 112+ bits |
| Nation-state and long-term classical safety | 112 bits | 128 bits |
| Bitcoin mnemonic generation | — | full 128-bit target |

These are engineering recommendations, not sharp boundaries. An extra bit doubles brute-force cost.

---

## 6. Evidence about sophisticated cryptocurrency actors

The FBI's September 2024 advisory “North Korea Aggressively Targeting Crypto Industry with Well-Disguised Social Engineering Attacks” describes DPRK operations using:

- extensive research on selected targets;
- personalized employment or investment approaches;
- impersonation and prolonged rapport-building;
- requests to execute scripts, packages, repositories, or custom software;
- malware deployment and network compromise;
- theft of cryptocurrency-related credentials and assets.

The advisory recommends keeping wallet identifiers, passwords, seed phrases, and private keys off Internet-connected devices. This is consistent with the primary real-world threat: **steal or observe the key rather than enumerate a cryptographic search space**.

There is no public evidence in that advisory that Lazarus Group can brute-force properly generated 112- or 128-bit mnemonic entropy. “Nation-state actor” should therefore not be translated into an unsupported seed-guess rate. The $10^{12}$/s and $10^{15}$/s rows above are hypothetical safety margins.

---

## 7. Applying the dice-bias model

The formulas and complete $\varepsilon$-to-entropy tables are maintained in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md#53-illustrative-model-b-bounded-multiplicative-bias). This document consumes those entropy totals rather than deriving them again.

For threat interpretation, two representative outputs are sufficient:

- at $\varepsilon\le0.05$, the canonical analysis gives approximately 119 bits for binary quantization and a 122.6-bit conservative lower bound for Oren's variable-length mapping, both far beyond plausible classical exhaustive search;
- at $\varepsilon=0.10$, binary falls slightly below the 112-bit benchmark while the lower bound for Oren's variable-length mapping remains above it, making the distinction relevant to conservative long-term policy.

These statements require both the final-outcome bound and the independence assumption to hold. They do not establish either physical assumption.

This does not eliminate operational risks such as:

- cameras or observers during generation;
- malicious or compromised wallet hardware;
- insecure computers used for conversion;
- photographed or stolen backups;
- weak BIP-39 passphrases;
- supply-chain manipulation;
- predictable human deviations from the prescribed procedure.

At entropy levels above approximately 112 bits, these risks dominate brute force.

---

## 8. Standards comparison

NIST SP 800-57 Part 1 Revision 5 recognizes 112-bit and 128-bit security-strength categories. In practical terms:

- 112 bits is beyond foreseeable classical exhaustive search;
- 128 bits provides additional long-term margin;
- secp256k1 itself is generally treated as providing approximately 128 bits of classical security.

A 12-word mnemonic with approximately 128 bits of actual min-entropy is therefore aligned with Bitcoin's classical elliptic-curve security. A 24-word mnemonic contains 256 source bits, but it does not raise secp256k1's classical security above approximately 128 bits.

---

## 9. Quantum qualification

An ideal Grover search changes generic exhaustive-search query complexity from approximately $2^h$ to $2^{h/2}$. This does not imply that 128-bit mnemonics are currently quantum-crackable:

- no cryptographically relevant fault-tolerant quantum computer is known;
- each query must reversibly implement the complete verification computation;
- error correction and circuit depth impose enormous overhead;
- Grover search does not parallelize as efficiently as classical search.

Bitcoin also faces a distinct future quantum issue: Shor's algorithm against secp256k1 public keys. Increasing mnemonic entropy does not solve that protocol-level problem. NIST finalized its first post-quantum standards in 2024 and recommends migration planning, but this is not evidence of a present mnemonic brute-force capability.

---

## 10. Conclusions

1. Use min-entropy rather than Shannon entropy for brute-force safety claims.
2. Treat actor-specific guess rates as scenarios unless backed by complete-candidate benchmarks.
3. Below 64 bits can be dangerous; 80 bits is not an appropriate new cryptographic target despite being hard today.
4. At least 112 bits is a conservative long-term objective; 128 bits is preferred.
5. A bounded-dice result of $\varepsilon\le0.05$ leaves approximately 119 bits for a 12-word binary method or at least 122.6 bits under the conservative Oren's variable-length mapping recurrence; neither is plausibly classically brute-forceable.
6. For sophisticated cryptocurrency actors, key theft, malware, social engineering, and operational compromise are more realistic than exhaustive seed search.

## References

- [NIST SP 800-57 Part 1 Revision 5: Recommendation for Key Management](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- [NIST: First Three Finalized Post-Quantum Encryption Standards](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
- [FBI IC3: North Korea Aggressively Targeting Crypto Industry with Well-Disguised Social Engineering Attacks](https://www.ic3.gov/PSA/2024/PSA240903)
- [BIP-39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
