# Practical implications: choosing a dice procedure for BIP-39

Document navigation:

- [Overview](../README.md)
- Previous: [Attacker capabilities versus mnemonic entropy](AttackerCapabilties.md)

---

## Executive recommendation

This synthesis applies four inputs owned by the preceding documents:

- the conversion formulas and canonical entropy tables in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md);
- the provisional $\varepsilon=0.01$ casino and $\varepsilon=0.10$ consumer scenarios in [Expected performance of real six-sided dice](ExpectedDicePerformace.md#4-plausible-analysis-scenarios);
- the [preferred lidded-box rolling protocol](RollingTechnique.md#31-preferred-lidded-box-method);
- the 112-bit conservative objective established in [Attacker capabilities versus mnemonic entropy](AttackerCapabilties.md#8-standards-comparison).

The scenario selection is deliberately asymmetric: $0.01$ is the central precision-dice scenario, while $0.10$ is the conservative consumer stress scenario. Neither is a product guarantee. All recommendations remain conditional on a valid final-outcome bound and independence between retained results.

The default recommendation is:

> Use base-4 rejection: map faces 1–4 to 00, 01, 10, and 11; discard faces 5–6; retain exactly 64 accepted symbols for 12 words or 128 for 24 words.

Base-4 rejection is preferred because it is transparent, manually auditable, directly compatible with the supplied bit-grouping and BIP-39 lookup sheets, and uses fewer expected physical results than binary quantization. Under the consumer stress scenario it remains above the 112-bit objective; 12-word binary quantization does not.

Ordinary binary quantization remains the simplest no-rejection alternative. It always uses exactly 128 or 256 physical results, but its 12-word min-entropy margin is small under the consumer-dice assumption.

Base 6 remains useful in two forms:

- **Full-integer conversion:** 50 or 100 results give the best roll efficiency and entropy margin, but converting a 50- or 100-digit base-6 integer manually is not realistically error-resistant. Use this only with verifiable hardware-wallet support (i.e. enter in two hardware-wallets from different vendors and compare results) or a small, reviewed, offline converter.
- **Manual per-word conversion:** groups of five base-6 digits can be converted separately to BIP-39 word indices using ordinary integer arithmetic. This needs 58 results for 12 words or 117 for 24 words, has no rejection, and avoids arbitrary-precision arithmetic. It is feasible by hand if every calculation is independently checked (e.g. with an off-line calculator [not on your phone or laptop/PC!]).

The consumer scenario is a stress assumption, not a product guarantee. If it lacks credible support for the actual dice-and-rolling setup, use a better-supported assumption or treat the numerical guarantee as unproven.

---

## 1. Ownership of decision inputs

This document does not repeat the underlying derivations or evidence:

- **Conversion behavior and entropy totals:** [DiceRollEntropyAnalysis.md](DiceRollEntropyAnalysis.md#5-results)
- **Physical-die evidence, scenario calibration, and statistical bounds:** [ExpectedDicePerformace.md](ExpectedDicePerformace.md)
- **Rolling dynamics, protocol, and process validation:** [RollingTechnique.md](RollingTechnique.md)
- **Threat model and interpretation of entropy levels:** [AttackerCapabilties.md](AttackerCapabilties.md)

The synthesis applies those inputs in this order:

1. reject a method if its conservative min-entropy is below 112 bits;
2. among methods that pass, prefer the least error-prone workflow;
3. then use cost and result count as tie-breakers.

---

## 2. Compared procedures

### 2.1 Binary quantization

Binary quantization emits one bit per die result and rejects nothing. Its [workflow](#61-binary-workflow) is the simplest fixed-length option, but the canonical entropy table shows that its 12-word result does not meet the 112-bit objective under the consumer stress scenario.

### 2.2 Base-4 rejection

Base-4 rejection emits two bits from each accepted result and discards faces 5 and 6. Its [workflow](#7-default-base-4-rejection-procedure) is manually simple and never invalidates earlier accepted work, but completion time is variable.

### 2.3 Full base 6 with global modulo conversion

For each result, subtract one so the faces become digits 0–5. Concatenate 50 digits for 12 words or 100 digits for 24 words and interpret them as one base-6 integer $X$. Produce the BIP-39 entropy integer

$$
Y=X\bmod2^L,
$$

where $L=128$ or $256$.

Because $6^k$ is not an exact multiple of $2^L$, this produces a small output imbalance even for ideal dice. The derivation and bound are maintained in the [conversion analysis](DiceRollEntropyAnalysis.md#41-naive-modulo-conversion).

There is no rejection, so every completed roll series is usable.

The mathematics is simple, but the hand computation is not. Repeatedly multiplying a 128- or 256-bit accumulator by six is too long and error-prone for a recommended paper-only procedure. This method therefore requires direct wallet support or a reviewed offline converter.

### 2.4 Base 6 with manual per-word modulo conversion

Instead of converting one enormous integer, process five base-6 digits at a time into one word-list index. The arithmetic is specified once in Section 8.1 below. No arbitrary-precision arithmetic is needed.

For the final word, only seven entropy bits are needed for a 12-word mnemonic and only three for a 24-word mnemonic. These use smaller versions of the same operation; the checksum occupies the remaining four or eight bits.

The method uses:

- $11\times5+3=58$ results for 12 words;
- $23\times5+2=117$ results for 24 words.

It has no rejection. Its disadvantage is that every arithmetic result must be checked carefully.

### 2.5 Base 6 with range rejection

Range rejection can produce exactly uniform output from ideal dice, but a complete block may be rejected. It does not automatically remove aggregate final-outcome bias. The acceptance calculations are owned by the [conversion analysis](DiceRollEntropyAnalysis.md#42-range-rejection); this synthesis does not recommend the extra retry burden.

### 2.6 Operational comparison

| Target | Procedure | Retained die results | Rejection risk | Main operational burden |
| ---: | --- | ---: | --- | --- |
| 12 words | Binary | 128 | None | Many manual results |
| 12 words | Base-4 rejection | 64 accepted; about 96 physical | 5–6 discarded individually | Simple bit-pair recording; variable completion time |
| 12 words | Base-6 global modulo | 50 | None | Direct wallet support or verified big-integer converter |
| 12 words | Base-6 per-word modulo | 58 | None | Repeated small-integer arithmetic and checking |
| 12 words | Base-6 rejection | 50 per attempt | 15.8% per complete attempt | Conversion plus possible complete retry |
| 24 words | Binary | 256 | None | Many manual results |
| 24 words | Base-4 rejection | 128 accepted; about 192 physical | 5–6 discarded individually | Simple bit-pair recording; variable completion time |
| 24 words | Base-6 global modulo | 100 | None | Direct wallet support or verified big-integer converter |
| 24 words | Base-6 per-word modulo | 117 | None | Repeated small-integer arithmetic and checking |
| 24 words | Base-6 rejection | 100 per attempt | 11.4% per complete attempt | Conversion plus possible complete retry |

The canonical quantitative comparison is in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md#5-results). This table is intentionally limited to operational burden.

---

## 3. Decision synthesis

| Situation | Recommended action |
| --- | --- |
| Consumer scenario $\varepsilon<0.10$ is credibly supported | Use base-4 rejection, global base-6 modulo, or manual per-word base 6 for 12 words; do not use 12-word binary as a 112-bit design |
| Consumer-dice performance is unknown | Do not claim a numerical guarantee; use the [statistical methodology](ExpectedDicePerformace.md#5-testing-five-identified-dice) to establish a bound or use a better-supported assumption |
| Maximum manual simplicity is preferred | Use base-4 rejection |
| Fixed completion length with no rejected results is essential | Use binary only when its canonical entropy result clears the selected objective |
| Minimum result count is preferred and a reviewed converter exists | Use global base-6 modulo |
| Paper-only base conversion with fewer results is preferred | Use manual per-word base 6 and independently check every group |
| No reviewed converter is available | Use base 4 or binary rather than improvised base conversion |

---

## 4. Shared operational requirements

### 4.1 Rolling

Every workflow below uses the [preferred lidded-box method](RollingTechnique.md#31-preferred-lidded-box-method), including its fixed reading order and invalid-batch rule. The [open-cast method](RollingTechnique.md#32-open-cast-alternative) is the documented fallback. Rolling details are not repeated here.

### 4.2 Standard BIP-39 completion

After a workflow has produced exactly 128 or 256 entropy bits:

1. calculate SHA-256 of the corresponding 16 or 32 bytes using a trusted offline implementation;
2. append the first four hash bits for 128-bit entropy or the first eight for 256-bit entropy;
3. split the resulting 132 or 264 bits into 11-bit groups;
4. interpret each group as a zero-based index into the official BIP-39 word list;
5. verify the mnemonic and recovered entropy with a separate trusted offline implementation or hardware wallet before funding.

### 4.3 Common security handling

Prepare the room and offline tools before generating secret values. Never submit dice results or mnemonic words to an online service. After independent verification, create and test the durable backup, then destroy unneeded paper and securely wipe or physically retire temporary digital storage.

---

## 5. Global base-6 workflow

Use this workflow only when direct base-6 wallet input or a reviewed offline arbitrary-precision converter is available. It is not the default paper-only recommendation.

| Target | Base-6 digits $k$ | Entropy length $L$ | Exact output width |
| ---: | ---: | ---: | ---: |
| 12 words | 50 | 128 bits | 16 bytes |
| 24 words | 100 | 256 bits | 32 bytes |

Required materials are dice satisfying the selected aggregate assumption, the rolling equipment specified in Section 4.1, paper, the official word list, and a verified offline tool that can preserve leading zeros and be wiped after use.

1. Complete the preparation in Section 4.3 and test the converter with nonsecret vectors.
2. Prepare $k$ numbered recording positions and a reading order fixed before rolling.
3. Follow the rolling protocol in Section 4.1. For every result, record face value minus one, producing a digit from 0 through 5.
4. Continue until exactly $k$ digits are recorded. In the final batch, retain only the predetermined first positions needed to reach $k$.
5. Read the string back twice, verify every digit is 0–5, and preserve leading zeros.
6. Enter the complete string into the verified offline tool as one base-6 integer $X$ and confirm that the displayed input matches the paper record.
7. Calculate
   $$Y=X\bmod2^L$$
   and render $Y$ at exactly the width shown above, preserving leading zeros.
8. Complete the standard BIP-39 and verification steps in Sections 4.2 and 4.3.

There is no rejected range: every correctly recorded $k$-digit series produces an output.

---

## 6. Binary procedure

Use this procedure when broad BIP-39 hardware-wallet compatibility and minimizing conversion mistakes are more important than roll count. It requires no base-6 support and no base conversion.

The supplied files support this workflow:

- [BitsToWords.pdf](../BitsToWords.pdf) or [BitsToWords.xlsx](../additional_ressources/BitsToWords.xlsx) provides spaces for the 11-bit word groups;
- [BIP39_Wordlist_Binary_Decimal_Searchable.pdf](../BIP39_Wordlist_Binary_Decimal_Searchable.pdf) or [BIP39_Wordlist_Binary_Decimal_Searchable.ods](../additional_ressources/BIP39_Wordlist_Binary_Decimal_Searchable.ods) maps each 11-bit or decimal zero-based index to its BIP-39 word.

These are recording and lookup aids, not checksum calculators. The checksum still requires a trusted offline SHA-256 implementation or a hardware-wallet feature designed to complete or validate the final word.

### 6.1 Binary workflow

1. Complete the common preparation in Section 4.3 using dice whose applicable aggregate bound has credible support.
2. Prepare 128 numbered bit positions for 12 words or 256 positions for 24 words.
3. Follow the rolling and ordering protocol in Section 4.1.
4. Record one bit per die:
   - face 1, 2, or 3: record 0;
   - face 4, 5, or 6: record 1.
5. Repeat until exactly 128 or 256 bits have been recorded. If the final batch is larger than the remaining spaces, use predetermined positions and ignore the rest.
6. Complete Sections 4.2 and 4.3.

This procedure never rejects a die result or a complete series. Its disadvantage is the larger number of results.

---

## 7. Default base-4 rejection procedure

This procedure uses the same bit sheets, word lookup, checksum process, and ordinary BIP-39 hardware-wallet entry as binary quantization.

### 7.1 Encoding

| Die face | Record |
| ---: | :--- |
| 1 | 00 |
| 2 | 01 |
| 3 | 10 |
| 4 | 11 |
| 5 or 6 | Nothing; reject this result |

### 7.2 Procedure with one or more dice

1. Complete the common preparation in Section 4.3 using dice whose applicable aggregate bound has credible support.
2. Prepare 128 numbered entropy-bit positions for 12 words or 256 positions for 24 words. Do not fill the checksum positions yet.
3. Follow the rolling and ordering protocol in Section 4.1.
4. Inspect every die in the predetermined order:
   - for face 1–4, write its two-bit pair into the next two empty positions;
   - for face 5 or 6, write nothing and continue to the next die.
5. Roll the full batch again. Previously accepted dice are not removed; every die may supply another symbol on every batch.
6. Continue until exactly 64 accepted symbols have filled 128 bits, or 128 accepted symbols have filled 256 bits.
7. In the final batch, process accepted results in the predetermined order only until the bit sheet is full. Ignore all later dice, regardless of their values.
8. Complete Sections 4.2 and 4.3.

### 7.3 Batch expectations

The canonical ideal and bounded-model expectations are in [Entropy from ideal and real dice](DiceRollEntropyAnalysis.md#34-batch-count). The operational comparison in Section 2.6 lists the result counts used by this synthesis.

Rejecting a result does not mean physically rerolling that die in isolation before reading the rest of the batch. Simply ignore its 5 or 6, finish processing the batch, and then roll the full set again. Rolling only the rejected dice would also work if die identities and order were handled consistently, but rerolling the full batch is simpler and less error-prone.

---

## 8. Manually feasible base-6-to-BIP-39 procedure

This procedure converts base 6 directly into BIP-39 word indices one group at a time. It avoids both a large-integer converter and direct base-6 support in the hardware wallet. Once the checksum has been completed, the resulting mnemonic is entered as ordinary BIP-39 words.

### 8.1 Common five-digit conversion

1. Convert each die face to a base-6 digit by subtracting one: face 1 becomes 0, face 2 becomes 1, through face 6 becoming 5.
2. Take five digits in their recorded order and label them $d_1,d_2,d_3,d_4,d_5$.
3. Calculate the same number in two independent ways:

   $$
   x=1296d_1+216d_2+36d_3+6d_4+d_5,
   $$

   and

   $$
   x=((((d_1\times6+d_2)\times6+d_3)\times6+d_4)\times6+d_5).
   $$

4. Stop and recalculate if the two answers differ.
5. While $x\ge2048$, subtract 2048. At most three subtractions are necessary. The remainder $w$ is between 0 and 2047.
6. Use $w$ as a **zero-based** BIP-39 index. Look it up in the supplied searchable BIP-39 table.

Example: the base-6 digits 1, 2, 3, 4, 5 give

$$
x=1296+432+108+24+5=1865.
$$

No subtraction is needed, so the word index is 1865. The example is public and must not be reused as secret entropy.

### 8.2 Twelve-word procedure

1. Complete the common preparation in Section 4.3.
2. Follow the rolling protocol in Section 4.1 and record exactly 58 base-6 digits using face minus one.
3. Divide the first 55 digits into eleven consecutive groups of five.
4. Convert each group using the common procedure in Section 8.1. The resulting indices select words 1 through 11.
5. For the final three digits $a,b,c$, calculate

   $$
   q=36a+6b+c
   $$

   in one calculation and $q=(6a+b)6+c$ in a second calculation. The answers must agree.
6. Calculate $r=q\bmod128$ by subtracting 128 once if $q\ge128$. This gives the final seven entropy bits as an integer from 0 through 127.
7. Concatenate the eleven 11-bit indices and the seven-bit representation of $r$, preserving leading zeros. These are the 128 entropy bits.
8. Calculate SHA-256 of the corresponding 16 bytes using a trusted offline implementation. Interpret the first four hash bits as an integer $c_4$ from 0 through 15.
9. Calculate the final word index

   $$
   w_{12}=16r+c_4.
   $$

10. Look up $w_{12}$ in the supplied BIP-39 table and append that word.
11. Verify the complete mnemonic's checksum on a separate trusted offline implementation or hardware wallet before funding it.
12. Complete the backup and cleanup requirements in Section 4.3.

This procedure has no rejection and always uses exactly 58 results.

### 8.3 Twenty-four-word procedure

1. Complete the common preparation in Section 4.3.
2. Follow the rolling protocol in Section 4.1 and record exactly 117 base-6 digits using face minus one.
3. Divide the first 115 digits into twenty-three consecutive groups of five.
4. Convert each group using the common procedure in Section 8.1. The resulting indices select words 1 through 23.
5. For the final two digits $a,b$, calculate $q=6a+b$.
6. Calculate $r=q\bmod8$ by subtracting 8 repeatedly until the result is between 0 and 7. This gives the final three entropy bits.
7. Concatenate the twenty-three 11-bit indices and the three-bit representation of $r$, preserving leading zeros. These are the 256 entropy bits.
8. Calculate SHA-256 of the corresponding 32 bytes using a trusted offline implementation. Interpret the first eight hash bits as an integer $c_8$ from 0 through 255.
9. Calculate the final word index

   $$
   w_{24}=256r+c_8.
   $$

10. Look up $w_{24}$ in the supplied BIP-39 table and append that word.
11. Verify the complete mnemonic's checksum on a separate trusted offline implementation or hardware wallet before funding it.
12. Complete the backup and cleanup requirements in Section 4.3.

This procedure has no rejection and always uses exactly 117 results.

### 8.4 Practical assessment

The small-block method is manually feasible, but not as simple as binary quantization. Its advantages are:

- no arbitrary-precision arithmetic;
- no software needed for base-6 conversion;
- no direct base-6 wallet support needed;
- fewer die results than binary;
- more margin than binary in the canonical consumer-scenario calculation.

Its disadvantages are:

- eleven or twenty-three independently checked arithmetic conversions;
- greater risk of an unnoticed calculation or transcription error;
- the checksum still cannot realistically be calculated without trusted SHA-256 support;
- the procedure is not a standard hardware-wallet input workflow and should be tested using public test data before real entropy is generated.

The base-4 procedure therefore remains the default compromise. Binary is the simplest no-rejection method, while manual base 6 is a reasonable roll-saving alternative for a careful user who independently verifies every group.

---

## 9. Implementation qualifications

1. **Any converter becomes security-critical.** It must preserve leading zeros, implement arithmetic exactly, hash the correct byte representation, and use the official word-list order.
2. **Modulo is intentional.** Do not replace it with decimal truncation, floating-point conversion, or an arbitrary substring of a binary representation.
3. **Test with nonsecret vectors first.** A tool that has not been independently verified should not receive real seed material.
4. **A BIP-39 passphrase is separate.** It may improve theft resistance but should not be used to excuse weak mnemonic generation.
5. **Compatibility means BIP-39 compatibility.** A wallet using another mnemonic standard cannot necessarily restore these words.

## References

- [BIP-39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
