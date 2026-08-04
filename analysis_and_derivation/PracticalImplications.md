# Practical implications: choosing a dice procedure for BIP-39

Document navigation:

- [Overview](../README.md)
- Previous: [Attacker capabilities versus mnemonic entropy](AttackerCapabilties.md)

---

## Executive recommendation

Under the provisional assumptions

- new casino-grade dice satisfy $\varepsilon<0.01$;
- acceptable consumer dice satisfy $\varepsilon<0.10$;
- at least approximately 110 bits of min-entropy are required;
- rolls are independent;
- every die used satisfies the applicable bound;

both dice classes can safely generate 12-word and 24-word BIP-39 mnemonics.

The default recommendation is:

> Use base-4 rejection: map faces 1–4 to 00, 01, 10, and 11; discard faces 5–6; retain exactly 64 accepted symbols for 12 words or 128 for 24 words.

Base-4 rejection is preferred as the default compromise because it is transparent, manually auditable, directly compatible with the supplied bit-grouping and BIP-39 lookup sheets, and uses approximately 25% fewer physical rolls than binary quantization with ideal dice. After checksum completion, the resulting words can be restored on any BIP-39-compatible hardware wallet.

Ordinary binary quantization remains the simplest no-rejection alternative. It always uses exactly 128 or 256 physical results, but its 12-word min-entropy margin is small under the consumer-dice assumption.

Base 6 remains useful in two forms:

- **Full-integer conversion:** 50 or 100 results give the best roll efficiency and entropy margin, but converting a 50- or 100-digit base-6 integer manually is not realistically error-resistant. Use this only with verifiable hardware-wallet support (i.e. enter in two hardware-wallets from different vendors and compare results) or a small, reviewed, offline converter.
- **Manual per-word conversion:** groups of five base-6 digits can be converted separately to BIP-39 word indices using ordinary integer arithmetic. This needs 58 results for 12 words or 117 for 24 words, has no rejection, and avoids arbitrary-precision arithmetic. It is feasible by hand if every calculation is independently checked (e.g. with an off-line calculator [not on your phone or laptop/PC!]).

Under the consumer-dice assumption, binary leaves approximately 110.4 bits for 12 words, base-4 rejection leaves approximately 114.5 bits, and manual per-word base 6 retains approximately 119.0 bits. Base 4 therefore improves both roll count and margin without introducing arithmetic conversion.

Because the consumer-dice assumption still needs validation, consumer dice should be preferred on cost only after their $\varepsilon<0.10$ bound has credible support. Otherwise use new casino-grade dice or treat the entropy guarantee as unproven.

---

## 1. Decision criteria

The priorities are applied in this order:

1. **Safety:** reject a procedure if its conservative min-entropy is materially below approximately 110 bits.
2. **Cost:** once safety is satisfied, prefer ordinary consumer dice over casino dice if their assumed performance has been validated.
3. **Operational simplicity and roll count:** avoid rejection and complete retrials; accept some additional rolls to reduce mistakes, but reconsider a simple method when it requires more than twice as many results.

The analysis uses min-entropy rather than Shannon entropy because min-entropy controls the probability of the attacker's best guess.

The recommendations are conditional. A label such as “casino grade” or “consumer die” is not itself a statistical proof of the assumed $\varepsilon$.

---

## 2. Provisional dice classes

For every face of every die, the bounded multiplicative model is

$$
\frac{1-\varepsilon}{6}\le p_i\le\frac{1+\varepsilon}{6}.
$$

The two working assumptions are:

| Dice class | Provisional bound | Permitted face-probability range | Status |
| --- | ---: | ---: | --- |
| Casino-grade precision dice | $\varepsilon<0.01$ | approximately 0.16500–0.16833 | Plausible scenario; not established by dimensional tolerance alone |
| Good consumer dice | $\varepsilon<0.10$ | approximately 0.15000–0.18333 | Stress scenario requiring validation for the actual dice and procedure |

The casino assumption provides more entropy margin. The consumer assumption is sufficient for all methods retained in this document, but only narrowly sufficient for a 12-word binary mnemonic. Casino dice are not required solely to reach the 110-bit objective if the consumer bound is credible.

Using several dice does not improve the guaranteed bound under the $\varepsilon$ model alone. Their imperfections may diversify in reality, but the conservative calculation allows aligned systematic bias. Multiple dice are still useful because they reduce the number of physical cup throws.

---

## 3. Compared procedures

### 3.1 Binary quantization

For each die result:

- faces 1, 2, or 3 become bit 0;
- faces 4, 5, or 6 become bit 1.

The guaranteed min-entropy per retained bit is

$$
1-\log_2(1+\varepsilon).
$$

No results are rejected. A 12-word mnemonic needs 128 results; a 24-word mnemonic needs 256.

### 3.2 Base-4 rejection

For each die result:

- face 1 becomes 00;
- face 2 becomes 01;
- face 3 becomes 10;
- face 4 becomes 11;
- faces 5 and 6 are discarded.

A 12-word mnemonic needs 64 accepted symbols and a 24-word mnemonic needs 128. With ideal dice, two thirds of results are accepted, so the expected physical-roll counts are 96 and 192. Completion time is variable, but rejection occurs one result at a time and never invalidates earlier work.

### 3.3 Full base 6 with global modulo conversion

For each result, subtract one so the faces become digits 0–5. Concatenate 50 digits for 12 words or 100 digits for 24 words and interpret them as one base-6 integer $X$. Produce the BIP-39 entropy integer

$$
Y=X\bmod2^L,
$$

where $L=128$ or $256$.

This method is called “naive modulo” because $6^k$ is not an exact multiple of $2^L$. Even ideal dice therefore produce a very small output imbalance. The conservative min-entropy bound accounts for that imbalance.

There is no rejection, so every completed roll series is usable.

The mathematics is simple, but the hand computation is not. Repeatedly multiplying a 128- or 256-bit accumulator by six is too long and error-prone for a recommended paper-only procedure. This method therefore requires direct wallet support or a reviewed offline converter.

### 3.4 Base 6 with manual per-word modulo conversion

Instead of converting one enormous integer, process five base-6 digits at a time. For digits $d_1,\ldots,d_5\in\{0,\ldots,5\}$, calculate

$$
x=1296d_1+216d_2+36d_3+6d_4+d_5
$$

and then calculate the BIP-39 index

$$
w=x\bmod2048.
$$

Because $0\le x\le7775$, the modulo operation is performed by subtracting 2048 repeatedly, at most three times. Each five-digit group directly produces one 11-bit BIP-39 group and hence one word-list index. No arbitrary-precision arithmetic is needed.

For the final word, only seven entropy bits are needed for a 12-word mnemonic and only three for a 24-word mnemonic. These use smaller versions of the same operation; the checksum occupies the remaining four or eight bits.

The method uses:

- $11\times5+3=58$ results for 12 words;
- $23\times5+2=117$ results for 24 words.

It has no rejection. Its disadvantage is that every arithmetic result must be checked carefully.

### 3.5 Base 6 with range rejection

Range rejection can produce exactly uniform output from ideal dice, but a complete block may be rejected. The simple block algorithm accepts approximately:

- 84.2% of 50-digit blocks for 128 bits;
- 88.6% of 100-digit blocks for 256 bits.

It does not automatically remove physical die bias. Because the no-rejection modulo procedure already exceeds the required security level, the extra retry rule is not justified for this practical objective.

### 3.6 Comparison

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

Binary requires

$$
\frac{128}{50}=\frac{256}{100}=2.56
$$

times as many retained results as global base-6 modulo. Binary requires approximately 2.2 times as many results as manual per-word base 6. Base-4 rejection avoids that conversion complexity while reducing expected physical rolls by approximately 25% compared with binary.

---

## 4. Conservative entropy results

### 4.1 Binary quantization

| Target | Dice assumption | Guaranteed min-entropy |
| ---: | --- | ---: |
| 12 words | Casino, $\varepsilon<0.01$ | greater than 126.16 bits |
| 12 words | Consumer, $\varepsilon<0.10$ | greater than 110.40 bits |
| 24 words | Casino, $\varepsilon<0.01$ | greater than 252.33 bits |
| 24 words | Consumer, $\varepsilon<0.10$ | greater than 220.80 bits |

The 12-word consumer case passes the approximate 110-bit requirement by only 0.40 bits. It should not be accepted if $\varepsilon=0.10$ is merely a point estimate rather than a defensible upper bound.

### 4.2 Base-4 rejection

For acceptance probability $A=p_1+p_2+p_3+p_4$, an accepted face has probability $p_i/A$. Under the bounded model,

$$
\frac{2-\varepsilon}{3}\le A\le\frac{2+\varepsilon}{3}
$$

and the min-entropy per accepted symbol is at least

$$
\log_2\frac{4-2\varepsilon}{1+\varepsilon}.
$$

| Target | Dice assumption | Accepted symbols | Conservative min-entropy | Worst expected physical rolls |
| ---: | --- | ---: | ---: | ---: |
| 12 words | Casino, $\varepsilon<0.01$ | 64 | greater than 126.62 bits | less than 96.49 |
| 12 words | Consumer, $\varepsilon<0.10$ | 64 | greater than 114.46 bits | less than 101.06 |
| 24 words | Casino, $\varepsilon<0.01$ | 128 | greater than 253.24 bits | less than 192.97 |
| 24 words | Consumer, $\varepsilon<0.10$ | 128 | greater than 228.93 bits | less than 202.11 |

The discarded results contribute no entropy. Rejection corrects the six-to-four radix mismatch, not unknown physical bias among faces 1–4.

### 4.3 Base-6 modulo

With $k$ base-6 digits, the raw min-entropy is at least

$$
k\left[\log_2 6-\log_2(1+\varepsilon)\right].
$$

Modulo conversion maps at most three 50-digit inputs to one 128-bit output and at most six 100-digit inputs to one 256-bit output. Therefore

$$
H_\infty(Y)\ge
H_\infty(X)-
\log_2\left\lceil\frac{6^k}{2^L}\right\rceil.
$$

| Target | Dice assumption | Conservative output min-entropy |
| ---: | --- | ---: |
| 12 words | Casino, $\varepsilon<0.01$ | greater than 126.95 bits |
| 12 words | Consumer, $\varepsilon<0.10$ | greater than 120.79 bits |
| 24 words | Casino, $\varepsilon<0.01$ | greater than 254.48 bits |
| 24 words | Consumer, $\varepsilon<0.10$ | greater than 242.16 bits |

All four cases exceed the 110-bit requirement comfortably. The 12-word consumer case has approximately 10.8 bits of margin, compared with only 0.4 bits under binary quantization.

### 4.4 Manual per-word base-6 modulo

Each full five-digit group has at least

$$
5[\log_2 6-\log_2(1+\varepsilon)]-\log_2 4
$$

bits of min-entropy after reduction modulo 2048, because no output has more than four preimages. The shortened final group is bounded similarly.

| Target | Dice assumption | Results | Conservative output min-entropy |
| ---: | --- | ---: | ---: |
| 12 words | Casino, $\varepsilon<0.01$ | 58 | greater than 126.10 bits |
| 12 words | Consumer, $\varepsilon<0.10$ | 58 | greater than 118.95 bits |
| 24 words | Casino, $\varepsilon<0.01$ | 117 | greater than 252.44 bits |
| 24 words | Consumer, $\varepsilon<0.10$ | 117 | greater than 238.03 bits |

This loses somewhat more entropy than one global modulo operation, but it remains comfortably above the selected threshold and is genuinely feasible without arbitrary-precision arithmetic.

### 4.5 Why not reduce the roll count further?

It is mathematically possible to use fewer base-6 results and target only approximately 110 source bits. That would create a highly restricted subset of otherwise valid BIP-39 entropy strings and leave little safety margin for model or testing error.

Using the conventional 50 or 100 global base-6 results, or 58 or 117 results for manual per-word conversion, is preferred because it:

- preserves a substantial margin;
- avoids conspicuous fixed leading portions of the entropy string;
- keeps the procedure aligned with generating a full 128- or 256-bit BIP-39 entropy value;
- still uses fewer than half as many results as binary quantization.

---

## 5. Global base-6 option for a 12-word mnemonic

### 5.1 Applicability

Use 50 full base-6 results and reduce the resulting integer modulo $2^{128}$ only when the hardware wallet supports direct base-6 input or a reviewed offline converter is available. This is not the default paper-only recommendation.

Prefer good consumer dice if their $\varepsilon<0.10$ bound is credibly validated under the intended cup and surface procedure. Otherwise use new casino-grade precision dice under the provisional $\varepsilon<0.01$ assumption.

### 5.2 Reasoning

- **Safety:** consumer dice at the assumed bound provide more than 120.79 bits of output min-entropy, comfortably above approximately 110 bits.
- **Cost:** validated consumer dice meet the target, so more expensive casino dice add margin but are not necessary.
- **Roll count:** only 50 results are needed instead of 128 for binary quantization.
- **Compatibility:** most hardware wallets do not accept the 50 base-6 digits directly. The conversion must be completed before ordinary BIP-39 word entry.
- **Simplicity:** there is no rejection decision and no possibility of discarding all 50 results, but full-integer conversion is not reasonably convenient by hand.
- **Error resistance:** the required offline converter should display the entered base-6 string for verification before conversion.

### 5.3 Self-contained 12-word instructions

#### Materials for 12 words

- one or more six-sided dice satisfying the selected bias assumption;
- a dice cup;
- a hard, level rolling surface with enough room for the dice to tumble;
- paper and a pen;
- the official BIP-39 word list printed on paper;
- a verified offline tool capable of arbitrary-precision base conversion, SHA-256, and BIP-39 word lookup;
- an offline device that can be wiped after use.

#### Procedure for 12 words

1. **Prepare the room.** Remove cameras, phones, smart speakers, and other recording devices. Close curtains if necessary. Do not perform the procedure where another person can observe it.
2. **Prepare the offline device.** Disconnect networking before entering any secret values. Confirm that the converter has been tested with nonsecret test vectors. Do not use an online website.
3. **Prepare a recording sheet.** Number 50 spaces from 1 through 50. Decide the reading order before rolling. If multiple dice are distinguishable, use a fixed die order. If they are indistinguishable, read them by a fixed physical rule such as left to right after they stop.
4. **Roll vigorously.** Put all dice in the cup, shake thoroughly, and cast them so they tumble freely on the hard surface. Do not arrange or select dice based on their values.
5. **Record base-6 digits.** For each die result, write face value minus one:

   | Die face | Record |
   | ---: | ---: |
   | 1 | 0 |
   | 2 | 1 |
   | 3 | 2 |
   | 4 | 3 |
   | 5 | 4 |
   | 6 | 5 |

6. **Repeat until exactly 50 digits are recorded.** If the final batch contains more results than needed, retain the predetermined first positions and ignore the remainder. Never choose which results to retain after seeing their values.
7. **Verify the transcription.** Read the 50 recorded digits back twice. Every character must be between 0 and 5. Preserve leading zeros.
8. **Form the integer.** Enter the complete 50-character string into the verified offline tool as a base-6 integer $X$. Confirm that the tool echoes exactly the same string.
9. **Reduce to 128 bits.** Calculate
   $$Y=X\bmod2^{128}.$$
   Render $Y$ as exactly 128 binary bits or 16 bytes. Keep leading zero bits or bytes.
10. **Compute the BIP-39 checksum.** Calculate SHA-256 of the 16-byte value. Take the first four bits of the hash and append them to the 128 entropy bits. The result contains 132 bits.
11. **Create the words.** Split the 132 bits from left to right into twelve 11-bit groups. Interpret each group as an integer from 0 through 2047 and select the word with that zero-based index from the official BIP-39 word list.
12. **Verify independently offline.** Use a separate trusted offline wallet or implementation to check that the twelve words have a valid BIP-39 checksum and reproduce the expected entropy. Never submit the words to a website.
13. **Make the permanent backup.** Copy the words accurately to the intended durable backup. Check spelling and order at least twice.
14. **Remove temporary secrets.** Destroy the paper containing raw dice digits unless it is intentionally part of the security design. Securely wipe or physically retire temporary digital storage used for conversion. Reconnect the device only after secrets and recoverable temporary files are removed.
15. **Test recovery before funding.** Restore the mnemonic on a trusted offline device and verify receive addresses before sending significant funds.

There is no rejected range in this procedure. Every correctly recorded 50-digit series produces a result.

---

## 6. Global base-6 option for a 24-word mnemonic

### 6.1 Applicability

Use 100 full base-6 results and reduce the resulting integer modulo $2^{256}$ only when the hardware wallet supports direct base-6 input or a reviewed offline converter is available. This is not the default paper-only recommendation.

As with the 12-word case, prefer validated consumer dice for cost. Use casino-grade dice when the consumer bound is unavailable, insufficiently supported, or additional physical-quality margin is desired.

### 6.2 Reasoning

- **Safety:** even consumer dice at $\varepsilon<0.10$ provide more than 242.16 bits of conservative output min-entropy.
- **Overall Bitcoin strength:** this is far above the approximate 128-bit classical security of secp256k1. A 24-word mnemonic does not make the elliptic-curve layer stronger than approximately 128 bits.
- **Cost:** consumer dice satisfy the entropy target under the assumption; casino dice are optional margin.
- **Roll count:** 100 results replace 256 binary results.
- **Compatibility:** most hardware wallets do not accept the 100 base-6 digits directly. The conversion must be completed before ordinary BIP-39 word entry.
- **Simplicity:** no rejection or complete retry is possible, but the 256-bit hand conversion is not reasonably convenient.

### 6.3 Self-contained 24-word instructions

#### Materials for 24 words

- one or more six-sided dice satisfying the selected bias assumption;
- a dice cup;
- a hard, level rolling surface with enough room for the dice to tumble;
- paper and a pen;
- the official BIP-39 word list printed on paper;
- a verified offline tool capable of arbitrary-precision base conversion, SHA-256, and BIP-39 word lookup;
- an offline device that can be wiped after use.

#### Procedure for 24 words

1. **Prepare the room.** Remove cameras, phones, smart speakers, and other recording devices. Prevent observation through doors or windows.
2. **Prepare the offline device.** Disconnect all networking before entering secret values. Verify the converter with nonsecret test vectors. Never use an online conversion or mnemonic website.
3. **Prepare a recording sheet.** Number 100 spaces from 1 through 100. Fix the reading order before rolling. Use fixed die identity order for distinguishable dice or a fixed physical order for indistinguishable dice.
4. **Roll vigorously.** Shake all dice thoroughly in the cup and cast them so they tumble freely. Do not manipulate their orientation or select results based on value.
5. **Record base-6 digits.** Convert every die face by subtracting one:

   | Die face | Record |
   | ---: | ---: |
   | 1 | 0 |
   | 2 | 1 |
   | 3 | 2 |
   | 4 | 3 |
   | 5 | 4 |
   | 6 | 5 |

6. **Repeat until exactly 100 digits are recorded.** In an oversized final batch, keep only positions chosen by the fixed rule in advance. Ignore the other results regardless of their values.
7. **Verify the transcription.** Read the entire 100-digit string back twice. Every digit must be 0–5. Do not remove leading zeros.
8. **Form the integer.** Enter the exact 100-character string into the verified offline tool as one base-6 integer $X$. Compare the displayed input with the paper record.
9. **Reduce to 256 bits.** Calculate
   $$Y=X\bmod2^{256}.$$
   Render $Y$ as exactly 256 binary bits or 32 bytes, preserving all leading zeros.
10. **Compute the BIP-39 checksum.** Calculate SHA-256 of the 32-byte value. Take the first eight bits of the hash and append them to the 256 entropy bits. The result contains 264 bits.
11. **Create the words.** Split the 264 bits from left to right into twenty-four 11-bit groups. Interpret each group as an integer from 0 through 2047 and select the word with that zero-based index from the official BIP-39 word list.
12. **Verify independently offline.** Confirm the checksum and recovered entropy using a separate trusted offline wallet or implementation. Never type the mnemonic into an online service.
13. **Make the permanent backup.** Transfer the 24 words to durable backup media and verify every word and its position at least twice.
14. **Remove temporary secrets.** Destroy the raw-digit sheet unless intentionally retained. Securely wipe or physically retire temporary digital storage before reconnecting any device.
15. **Test recovery before funding.** Restore the mnemonic offline and verify derived receive addresses before transferring significant value.

There is no rejected range in this procedure. Every correctly recorded 100-digit series produces a result.

---

## 7. Binary procedure

Use this procedure when broad BIP-39 hardware-wallet compatibility and minimizing conversion mistakes are more important than roll count. It requires no base-6 support and no base conversion.

The supplied files support this workflow:

- [BitsToWords.pdf](../BitsToWords.pdf) or [BitsToWords.xlsx](../additional_ressources/BitsToWords.xlsx) provides spaces for the 11-bit word groups;
- [BIP39_Wordlist_Binary_Decimal_Searchable.pdf](../BIP39_Wordlist_Binary_Decimal_Searchable.pdf) or [BIP39_Wordlist_Binary_Decimal_Searchable.ods](../additional_ressources/BIP39_Wordlist_Binary_Decimal_Searchable.ods) maps each 11-bit or decimal zero-based index to its BIP-39 word.

These are recording and lookup aids, not checksum calculators. The checksum still requires a trusted offline SHA-256 implementation or a hardware-wallet feature designed to complete or validate the final word.

### 7.1 Self-contained binary instructions

1. Use dice whose applicable $\varepsilon$ bound has credible support.
2. Remove cameras, phones, observers, and networked devices from the generation area.
3. Prepare 128 numbered bit positions for 12 words or 256 positions for 24 words.
4. Decide the order in which multiple dice will be read before rolling.
5. Shake the dice thoroughly in a cup and cast them so they tumble freely.
6. Read the dice using the predetermined order.
7. Record one bit per die:
   - face 1, 2, or 3: record 0;
   - face 4, 5, or 6: record 1.
8. Repeat until exactly 128 or 256 bits have been recorded. If the final batch is larger than the remaining spaces, use predetermined positions and ignore the rest.
9. For 128 bits, calculate SHA-256 of the corresponding 16 bytes and append the first four hash bits. For 256 bits, hash the corresponding 32 bytes and append the first eight hash bits.
10. Split the resulting 132 or 264 bits into 11-bit groups and map each zero-based value to the official BIP-39 word list.
11. Verify the checksum and recovery using a trusted offline wallet or implementation.
12. Create and verify the durable backup, remove all temporary secret material, and test recovery before funding.

This procedure never rejects a die result or a complete series. Its disadvantage is the larger number of results.

---

## 8. Default base-4 rejection procedure

This procedure uses the same bit sheets, word lookup, checksum process, and ordinary BIP-39 hardware-wallet entry as binary quantization.

### 8.1 Encoding

| Die face | Record |
| ---: | :--- |
| 1 | 00 |
| 2 | 01 |
| 3 | 10 |
| 4 | 11 |
| 5 or 6 | Nothing; reject this result |

### 8.2 Procedure with one or more dice

1. Use dice whose applicable $\varepsilon$ bound has credible support.
2. Remove cameras, phones, observers, and networked devices from the generation area.
3. Prepare 128 numbered entropy-bit positions for 12 words or 256 positions for 24 words. Do not fill the checksum positions yet.
4. Before rolling, define a permanent order in which the dice will be read. Distinguishable dice can use identity order; otherwise use a fixed physical rule such as left to right.
5. Shake all dice thoroughly in a cup and cast them so they tumble freely.
6. Inspect every die in the predetermined order:
   - for face 1–4, write its two-bit pair into the next two empty positions;
   - for face 5 or 6, write nothing and continue to the next die.
7. Roll the full batch again. Previously accepted dice are not removed; every die may supply another symbol on every batch.
8. Continue until exactly 64 accepted symbols have filled 128 bits, or 128 accepted symbols have filled 256 bits.
9. In the final batch, process accepted results in the predetermined order only until the bit sheet is full. Ignore all later dice, regardless of their values. Never select which accepted results to retain after seeing them.
10. For 128 bits, calculate SHA-256 of the corresponding 16 bytes and append the first four hash bits. For 256 bits, hash the corresponding 32 bytes and append the first eight hash bits.
11. Split the resulting 132 or 264 bits into 11-bit groups and use the supplied searchable BIP-39 table to find each word.
12. Verify the checksum and recovery with a separate trusted offline implementation or hardware wallet before funding.
13. Create and verify the durable backup, remove temporary secret material, and test recovery.

### 8.3 Batch expectations

With ideal dice:

| Dice per batch | Accepted symbols per batch, average | Batch-equivalents, 12 words | Batch-equivalents, 24 words |
| ---: | ---: | ---: | ---: |
| 1 | 0.67 | 96.0 | 192.0 |
| 5 | 3.33 | 19.2 | 38.4 |
| 6 | 4.00 | 16.0 | 32.0 |

The last two columns are expected physical-roll counts divided by the batch size, not exact expected whole-batch counts. A whole final batch creates a small unused-results overhead. A batch can contain zero accepted results or can accept every die. Under $\varepsilon<0.10$, the worst batch-equivalents rise to approximately 20.21 and 40.42 with five dice, or 16.84 and 33.68 with six dice.

Rejecting a result does not mean physically rerolling that die in isolation before reading the rest of the batch. Simply ignore its 5 or 6, finish processing the batch, and then roll the full set again. Rolling only the rejected dice would also work if die identities and order were handled consistently, but rerolling the full batch is simpler and less error-prone.

---

## 9. Manually feasible base-6-to-BIP-39 procedure

This procedure converts base 6 directly into BIP-39 word indices one group at a time. It avoids both a large-integer converter and direct base-6 support in the hardware wallet. Once the checksum has been completed, the resulting mnemonic is entered as ordinary BIP-39 words.

### 9.1 Common five-digit conversion

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

### 9.2 Twelve-word procedure

1. Prepare the private generation area, dice, cup, recording paper, checksum method, and printed lookup materials as described for the binary procedure.
2. Roll and record exactly 58 base-6 digits using face minus one. Predetermine the reading order for multiple dice.
3. Divide the first 55 digits into eleven consecutive groups of five.
4. Convert each group using the common procedure in Section 9.1. The resulting indices select words 1 through 11.
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

This procedure has no rejection and always uses exactly 58 results.

### 9.3 Twenty-four-word procedure

1. Prepare the private generation area, dice, cup, recording paper, checksum method, and printed lookup materials as described for the binary procedure.
2. Roll and record exactly 117 base-6 digits using face minus one. Predetermine the reading order for multiple dice.
3. Divide the first 115 digits into twenty-three consecutive groups of five.
4. Convert each group using the common procedure in Section 9.1. The resulting indices select words 1 through 23.
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

This procedure has no rejection and always uses exactly 117 results.

### 9.4 Practical assessment

The small-block method is manually feasible, but not as simple as binary quantization. Its advantages are:

- no arbitrary-precision arithmetic;
- no software needed for base-6 conversion;
- no direct base-6 wallet support needed;
- approximately 55% fewer die results than binary;
- more entropy margin than binary under the consumer-dice assumption.

Its disadvantages are:

- eleven or twenty-three independently checked arithmetic conversions;
- greater risk of an unnoticed calculation or transcription error;
- the checksum still cannot realistically be calculated without trusted SHA-256 support;
- the procedure is not a standard hardware-wallet input workflow and should be tested using public test data before real entropy is generated.

The base-4 procedure therefore remains the default compromise. Binary is the simplest no-rejection method, while manual base 6 is a reasonable roll-saving alternative for a careful user who independently verifies every group.

---

## 10. Decision table

| Situation | Recommended action |
| --- | --- |
| Consumer dice have a credible $\varepsilon<0.10$ bound | Prefer base-4 rejection for a simple method with approximately 114.5 bits of 12-word min-entropy |
| Consumer-dice performance is unknown | Do not claim the calculated guarantee; test them or use credible casino-grade dice |
| Casino dice plausibly satisfy $\varepsilon<0.01$ | Base 4 and binary both provide near-full target entropy; base 4 uses fewer expected rolls |
| No verified offline big-integer converter is available | Use base 4, binary, or manual per-word base 6 |
| Hardware wallet lacks direct base-6 input | Use base 4 or binary, or complete manual per-word conversion before entering ordinary BIP-39 words |
| Avoiding complete-block retries is important | Use base 4, binary, or modulo; base 4 rejects only individual results |
| Maximum simplicity with fewer expected rolls is preferred | Use base-4 rejection |
| Fixed completion length with no rejected results is essential | Use binary quantization |
| Rolling batches of five or six dice | Use base 4 with a fixed reading order; ignore 5–6 and roll the full batch again |
| Minimum roll count is preferred and a reviewed converter or direct wallet support exists | Use global base-6 modulo |
| Paper-only base conversion with fewer rolls is preferred | Use manual per-word base-6 modulo and independently check every group |
| Dice identities are visible during generation | Use a fixed identity order; do not count permutation as entropy |
| Dice identities are hidden | Hidden ordering may help, but do not credit it in the guaranteed bound |

---

## 11. Important qualifications

1. **The dice assumptions remain provisional.** Manufacturing descriptions do not establish $\varepsilon$ directly.
2. **Independence is assumed.** Controlled throws or serial correlation invalidate the simple additive entropy calculation.
3. **Any converter becomes security-critical.** It must preserve leading zeros, implement arithmetic exactly, hash the correct byte representation, and use the official word-list order.
4. **Modulo is intentional.** Do not replace it with decimal truncation, floating-point conversion, or taking an arbitrary substring of a binary representation.
5. **A BIP-39 passphrase is separate.** It may improve theft resistance but should not be used to excuse weak mnemonic generation.
6. **Operational compromise dominates at high entropy.** Observation, malware, malicious hardware, and backup theft are much more plausible than brute force once min-entropy exceeds approximately 110 bits.
7. **Test with nonsecret vectors first.** A tool that has not been independently verified should not receive real seed material.
8. **“All wallets” means BIP-39-compatible wallets.** A wallet using another mnemonic standard cannot necessarily restore a BIP-39 mnemonic.
9. **Base-4 rejection is conditional sampling, not bias removal.** It makes ideal dice exactly uniform over four symbols, but accepted outputs from biased dice remain biased.

## References

- [BIP-39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- [NIST SP 800-57 Part 1 Revision 5: Recommendation for Key Management](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- [NIST SP 800-90B: Recommendation for Entropy Sources](https://csrc.nist.gov/pubs/sp/800/90/b/final)
