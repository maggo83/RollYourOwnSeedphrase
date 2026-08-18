# Roll your own BIP-39 seed phrase with dice

Roll Your Own Seedphrase aims at providing a simple guide on how to obtain your own bitcoin seedphrase from dice
- in a simple-as-possible way
- with clear emphasis on what is needed to stay secure (i.e. generate sufficient entropy)
- with tools most people have readily available (hence 6-sided dice, possibly non-casino-grade)
- with as little dependence on third parties as possible (hence e.g. no reliance on hw wallets converting dice rolls to bits/seed words)
- while still being grounded / backed by actual research to ensure it is secure enough

# Derivation from analysis

If you only want to generate your seed and care only about the "how" and not so much about the "why", you can skip this chapter and go directly to the next.

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

# Standalone practical guide

[Printable quick guide](HowToRollYourOwnSeedphrase.pdf) is the formatted, print-friendly standalone procedure for generating a mnemonic with dice and the supplied worksheets. The original [plain-text version](HowToRollYourOwnSeedphrase.txt) remains available for simple offline reading, but is not mandatory to read.

The visual guide's canonical HTML, CSS, JavaScript, and assets live in `guide-src/`. The root-level `build-guides.py` composes shared fragments with the online Steps 3–5 workflow or the offline combined Step 3 workflow. The root `index.html` is the single generated online compatibility output.

Supporting printable material:

- [Bit-to-word worksheets](BitsToWords.pdf) for recording 12- or 24-word entropy bits;
- [Searchable BIP-39 binary and decimal word list](BIP39_Wordlist_Binary_Decimal_Searchable.pdf) for converting each 11-bit index into its BIP-39 word.
- [Printable quick guide](HowToRollYourOwnSeedphrase.pdf) as a quick reference on how to use the procedure and worksheets.

### Offline edition

An English-only, self-contained edition of the visual guide converts entered dice results into bits and BIP39 words, including the deterministic final-word checksum, on a permanently offline machine. It has automated verification, but it is **not independently reviewed, signed, or released yet**. THIS IS ONLY INTENDED FOR KNOWLEDGEABLE USERS WHO CAN SETUP AND MAINTAIN A PERMANENTLY OFFLINE MACHINE. IF YOU DO NOT KNOW HOW TO DO THAT, DO NOT USE THE OFFLINE EDITION. YOU WILL LOSE ALL YOUR BITCOIN.

Before any future release is used, follow the complete [offline-edition acquisition, GPG verification, transfer, and startup instructions](offline-package/README.md). The offline edition is intended only for a dedicated machine that has never been connected and will never be connected to the internet or another untrusted network; otherwise, funds may be at risk.

For development and review with **dummy data only**, run `python3 build-guides.py offline` from the repository root, then open `dist/offline/index.html` directly in a browser. No web server is required. Do not use this locally generated, unsigned build with real seed material.

## Source and builds

Canonical HTML and shared assets are stored under `guide-src/`. The root-level `build-guides.py` declares the exact ordered fragment list for each target: online uses the shared shell, Steps 1–4, the online wallet Step 5, Step 6, and the shared ending; offline inserts Step 0, replaces online Steps 3–5 with a combined dice-entry and bits-to-words Step 3, then completes at Step 4. The root `index.html` is generated online compatibility output and must not be edited. Both editions are complete static outputs: no fragment is loaded at runtime. Run `python3 offline-package/verify.py` after changing any source.

## Visual guide

The interactive version of the procedure is available on [GitHub Pages](https://maggo83.github.io/RollYourOwnSeedphrase/). Read it before generating a real seed phrase, or use it for a dry run first.

# Important qualification

The numerical guarantees depend on explicit assumptions about the dice, the way they are rolled, and independence between results. Product labels alone do not prove those assumptions. Regardless of the mathematical method, observation, malware, compromised hardware, transcription mistakes, and insecure backups can be more realistic threats than brute force.

## Security

Report vulnerabilities privately and verify future release signatures as described in [SECURITY.md](SECURITY.md). The release-signing fingerprint is `F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5`, independently published by [@MarcoKruse6 on X](https://x.com/MarcoKruse6).

## License

Project-authored files are available under the [Grug 2-Clause License](LICENSE):

1. do what want
2. not sue grug

Third-party material retains the license stated in its accompanying notice.
