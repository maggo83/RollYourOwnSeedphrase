# Roll your own BIP-39 seed phrase with dice

Roll Your Own Seedphrase aims at providing a simple guide on how to obtain your own bitcoin seedphrase from dice
- in a simple-as-possible way
- with clear emphasis on what is needed to stay secure (i.e. generate sufficient entropy)
- with tools most people have readily available (hence 6-sided dice, possibly non-casino-grade)
- with as little dependence on third parties as possible (hence e.g. no reliance on hw wallets converting dice rolls to bits/seed words)
- while still being grounded / backed by actual research to ensure it is secure enough

## Where to start?

This depends on what your goal is. Here are the scenarios we have in mind:

- You are just starting to learn about seed generation, and want to know asap HOW to: Use the [visual guide](#visual-guide) section to learn the method. Later, for a real seedphrase, use the [printable quick guide](#standalone-practical-guide) [it is also linked in the visual guide].
- You have experience with seed generation and directly want to generate a real seedphrase: Use the [Standalone practical guide](#standalone-practical-guide).
- You really want to understand the underlying research and reasoning behind the method: Read the [Derivation from analysis](#derivation-from-analysis) section below.
- You are an advanced Bitcoiner who knows his shit and has a permanently offline computer and want to generate a seedphrase on it: Use the [Offline edition](#offline-edition) section below.

# Derivation from analysis

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

# Visual guide

The interactive introductory version of the procedure is available on [GitHub Pages](https://maggo83.github.io/RollYourOwnSeedphrase/). Use it to learn the method or for a dry run. For a real seedphrase, use the [printable quick guide](HowToRollYourOwnSeedphrase.pdf) (also linked in the visual guide).

# Standalone practical guide

[Printable quick guide](HowToRollYourOwnSeedphrase.pdf) is the formatted, print-friendly standalone procedure for generating a mnemonic with dice and the supplied worksheets.

Required printable material:

- [Bit-to-word worksheets](BitsToWords.pdf) for recording 12- or 24-word entropy bits;
- [Searchable BIP-39 binary and decimal word list](BIP39_Wordlist_Binary_Decimal_Searchable.pdf) for converting each 11-bit index into its BIP-39 word.
- [Printable quick guide](HowToRollYourOwnSeedphrase.pdf) as a quick reference on how to use the procedure and worksheets.

# Offline edition

The English-only, self-contained offline edition converts entered dice results into bits and BIP39 words, including the deterministic final-word checksum. It is intended exclusively for a dedicated, permanently offline machine that has never connected and will never connect to the internet or another untrusted network.
IF YOU DO NOT KNOW WHAT THIS MEANS, DO NOT USE THE OFFLINE EDITION. The offline edition is a convenience tool for experts. It is not intended for the average user or use on a connected development machine or any other computer that has ever been online. IF YOU USE IT WRONGLY ALL YOUR BITCOIN MAY BE LOST.

The implementation has automated verification but has not received independent security review. Use it at your own risk under the project's [Grug 2-Clause License](LICENSE). See the [offline-edition README](offline-package/README.md) for its scope and the complete acquisition, GPG verification, transfer, and startup instructions.

# Source and builds

Canonical HTML structure and shared assets are stored under `guide-src/`. The root-level `build-guides.py` declares the exact ordered fragment list for each target: online builds English (`dist/en`) and German (`dist/de`) static editions; offline builds one English-only edition (`dist/offline`). Online translations are paired by fragment in `guide-src/i18n/catalog.json`, then generated as static output without a runtime fetch. `dist/index.html` is the one functional language selector. The root `index.html` is a generated local forwarder to it, while GitHub Pages publishes `dist/index.html` at its site root. Do not edit either file directly. The landing page is a language selector for English and informal German guide editions. Both editions always use the **one shared English BIP-39 word list**; German changes instructions and printable labels only. German printable material uses stable `-de` filenames for [the German quick guide](HowToRollYourOwnSeedphrase-de.pdf) and [German-labeled BitsToWords worksheet](BitsToWords-de.pdf). The English BIP-39 lookup list remains one shared artifact for every guide language.

The printable quick guides likewise use one template plus adjacent EN/DE section content in `print-src/quick-guide-template.html` and `print-src/quick-guide-content.json`. Committed printable artifacts are verified in CI by regenerating them with Chrome, LibreOffice, and `openpyxl`; ordinary users do not need build dependencies. Then run `python3 offline-package/verify.py` after changing guide source.

# Important qualification

The numerical guarantees depend on explicit assumptions about the dice, the way they are rolled, and independence between results. Product labels alone do not prove those assumptions. Regardless of the mathematical method, observation, malware, compromised hardware, transcription mistakes, and insecure backups can be more realistic threats than brute force.

## Security

Report vulnerabilities privately and verify future release signatures as described in [SECURITY.md](SECURITY.md). The release-signing fingerprint is `F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5`, independently published by [@MarcoKruse6 on X](https://x.com/MarcoKruse6).

## License

Project-authored files are available under the [Grug 2-Clause License](LICENSE):

1. do what want
2. not sue grug

Third-party material retains the license stated in its accompanying notice.
