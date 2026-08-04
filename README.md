# Roll your own BIP-39 seed phrase with dice

This project examines how to generate a BIP-39 mnemonic from six-sided dice, including the effects of imperfect dice, rolling technique and throw dynamics, different methods for converting rolls into bits, practical attacker capabilities, and the operational tradeoffs of each procedure.

The analysis distinguishes between:

- 12-word mnemonics with 128 independently generated entropy bits;
- 24-word mnemonics with 256 independently generated entropy bits;
- ideal and physically biased dice;
- physical dice and rolling technique as two contributors to the final-outcome distribution;
- binary quantization, base-4 rejection, and base-6 conversion;
- Shannon entropy and conservative min-entropy;
- mathematical security and practical generation risks.

## Analysis sequence

The documents are intended to be read in this order:

1. [Entropy from ideal and real dice](analysis_and_derivation/DiceRollEntropyAnalysis.md) develops the statistical model and compares the entropy produced by binary, base-4, and base-6 methods under several dice-bias models.
2. [Expected performance of real dice](analysis_and_derivation/ExpectedDicePerformace.md) reviews available evidence about physical dice, explains plausible bias assumptions, and discusses how difficult those assumptions are to validate experimentally.
3. [Rolling technique and throw dynamics](analysis_and_derivation/RollingTechnique.md) explains how handling, agitation, collisions, and settling affect the final outcomes and derives the common rolling protocol required by every encoding method.
4. [Attacker capabilities versus mnemonic entropy](analysis_and_derivation/AttackerCapabilties.md) relates the resulting min-entropy values to classical brute-force capabilities and realistic cryptocurrency threat actors.
5. [Practical implications](analysis_and_derivation/PracticalImplications.md) synthesizes the preceding results into method comparisons, recommendations, and detailed operational procedures.

## Standalone practical guide

[How to roll your own seed phrase](HowToRollYourOwnSeedphrase.txt) is the concise standalone result for someone who wants to generate a mnemonic using dice and the supplied printable worksheets. It describes direct bit-generation procedures and hardware-wallet-assisted checksum completion without requiring the reader to work through the full analysis first.

Supporting printable material:

- [Bit-to-word worksheets](BitsToWords.pdf) for recording 12- or 24-word entropy bits;
- [Searchable BIP-39 binary and decimal word list](BIP39_Wordlist_Binary_Decimal_Searchable.pdf) for converting each 11-bit index into its BIP-39 word.

## Important qualification

The numerical guarantees depend on explicit assumptions about the dice, the way they are rolled, and independence between results. Product labels alone do not prove those assumptions. Regardless of the mathematical method, observation, malware, compromised hardware, transcription mistakes, and insecure backups can be more realistic threats than brute force.
