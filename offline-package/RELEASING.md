# Release procedure

A public release must be signed with the key whose complete fingerprint is `F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5`, independently published on [@MarcoKruse6 on X](https://x.com/MarcoKruse6). Stable releases require independent security review of the offline derivation path. Before that review, only versions ending in `-rcN` may be published, and GitHub must mark them as prereleases whose notes state prominently that the implementation is not independently reviewed. Every release candidate still requires verified pinned sources, 12- and 24-word vectors, deterministic packaging, endpoint-security warnings, and complete release documentation. The package is a convenience tool, not a guarantee that a general-purpose computer is safe for secrets.

1. Review all source changes, especially the build scripts, Step 0, combined dice-entry and bits-to-words Step 3, SHA-256 implementation, and BIP39 source hash.
2. Run `python3 offline-package/verify.py` from a clean checkout and complete the browser checks in [TESTING.md](TESTING.md).
3. Commit and tag the reviewed source using the exact version prefixed by `v`, for example `v0.2.0-rc1`. Repeat verification from a fresh checkout of that exact tag.
4. On the controlled signing machine, run `python3 offline-package/release.py --version 0.2.0-rc1 --signing-key F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5`, substituting the reviewed version when it changes.
5. Repeat the release build in a second clean checkout and confirm that the ZIP and `SHA256SUMS` are byte-identical.
6. Upload the ZIP, `SHA256SUMS`, `SHA256SUMS.asc`, and `release-key.asc` from `dist/release/` as four assets of the same GitHub release.
7. Verify the uploaded assets exactly as an end user would before announcing the release.

Never publish a package built from a dirty working tree. Never put private-key material, a passphrase, or a revocation certificate in the repository or release assets.
