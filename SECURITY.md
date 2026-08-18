# Security policy

## Project status and scope

The offline edition handles highly sensitive BIP39 input, but no independently reviewed and GPG-signed offline release exists yet. Locally generated development builds must be used only with dummy data.

A valid release signature authenticates release files; it does not make a connected or compromised computer safe. Real seed material must be handled only on a dedicated machine that has never been connected and will never be connected to the internet or another untrusted network.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/maggo83/RollYourOwnSeedphrase/security/advisories/new) when available. If that channel is unavailable, contact [@MarcoKruse6 on X](https://x.com/MarcoKruse6) without publishing technical details, so a private channel can be established.

Include the affected release version or source commit, impact, reproduction steps, and a minimal proof of concept. Never include a real seed phrase, private key, wallet backup, passphrase, or other secret. Use dummy BIP39 vectors only.

Please allow time to investigate and coordinate a fix before public disclosure. General questions and documentation corrections that do not expose a vulnerability may use the public issue tracker.

## Release identity

The expected release-signing key fingerprint is:

```text
F621 C843 74E5 2EF6 F0F9  B6FA A310 A531 2D2E E2C5
```

The complete unspaced fingerprint is independently published on [@MarcoKruse6 on X](https://x.com/MarcoKruse6):

```text
F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5
```

Compare all 40 hexadecimal characters. A short key ID, matching name, or “Good signature” message alone is insufficient. Follow the offline edition's complete acquisition and verification procedure before trusting a future release.

## Supported versions

Until the first signed release, only the current source on the repository's default branch is maintained, and it is not approved for real seed material. After releases begin, security fixes will target the newest signed release; older releases should be treated as unsupported unless their release notes explicitly state otherwise.
