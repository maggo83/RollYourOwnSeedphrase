# Offline edition

> **Status: source implementation only.** Automated verification is present, but no GPG-signed offline edition has been released and the implementation has not received independent security review. Do not enter seed material into source files or locally generated builds. This README defines the access, verification, and startup instructions that must accompany the first release candidate.

The offline edition is a self-contained version of the visual guide for 12- and 24-word English BIP39 mnemonics only. It does not generate entropy or support other languages, BIP85, SLIP-39, passphrases, wallets, address derivation, or seed import/export. In Step 3, each accepted dice result is converted to bits, each complete 11-bit group is mapped to its BIP39 word, and the deterministic checksum completes the final word. The checksum adds no entropy.

You enter each physical die result in the fixed reading order. Faces are converted according to the selected base-4 or binary method, and bits fill the word rows automatically. For the final word, only 7 (or 3) bits come from dice; the remaining 4 (or 8) checksum bits are appended from the SHA-256 hash of the full entropy. All entered results, bits, and words stay in page memory only, are never logged or transmitted, and are cleared when you navigate away from Step 3 or close the guide.

For source review with **dummy data only**, run `python3 build-guides.py offline` from the repository root and open `dist/offline/index.html` directly in a browser. No server or installation is required. This development build is unsigned and must not receive real seed material.

## Critical machine requirement

Use the offline edition only on a dedicated machine that **has never been connected and will never be connected** to the internet, Wi-Fi, Bluetooth, Ethernet, mobile data, or any other untrusted network. An ordinary laptop temporarily placed in airplane mode is not suitable. If this requirement is not true, do not enter seed material: **your funds may be at risk**.

A valid release signature does not make an internet-connected or compromised computer safe. It establishes the origin and integrity of the downloaded files only.

Step 0's acknowledgement only blocks navigation. It cannot detect or prove isolation, and the browser, operating system, hardware, and removable media remain part of the trusted computing base.

## 1. Obtain the release

On a network-connected **staging computer that will never receive seed material**, open the repository's [official Releases page](https://github.com/maggo83/RollYourOwnSeedphrase/releases) and download these four assets from the same version:

- `RollYourOwnSeedphrase-offline-X.Y.Z-rcN.zip` — the complete offline guide;
- `SHA256SUMS` — the expected SHA-256 digest of the archive;
- `SHA256SUMS.asc` — the detached GPG signature over `SHA256SUMS`; and
- `release-key.asc` — the public release key.

Do not download an offline package from advertisements, URL shorteners, unofficial mirrors, direct messages, or links supplied in comments. Do not mix files from different releases.

Substitute the exact published release-candidate version for `X.Y.Z-rcN` in the commands below and check that every downloaded asset belongs to that same GitHub release.

## 2. Transfer the unopened release files

Treat the staging computer as untrusted. Its job is only to download and copy bytes:

1. Copy `RollYourOwnSeedphrase-offline-X.Y.Z-rcN.zip`, `SHA256SUMS`, `SHA256SUMS.asc`, and `release-key.asc` to newly prepared removable media used only for this purpose.
2. Eject the media cleanly.
3. Prefer media that can be made physically read-only after writing. Insert it into the dedicated, permanently offline machine only after enabling that protection, where available.

The staging computer may perform an **optional preliminary** signature and checksum check to catch an incomplete download, but that result is not trusted and does not replace verification on the offline machine. A compromised staging computer could falsify what it displays or alter files after checking them.

Removable media is itself an input into the offline machine. Use simple data-only media dedicated to this transfer and do not enable autorun. Verification reduces file-substitution risk, but cannot make malicious hardware or a vulnerable operating system safe.

## 3. Authenticate the release key on the offline machine

On another device, such as a smartphone, display the complete release-key fingerprint published on [@MarcoKruse6 on X](https://x.com/MarcoKruse6). The expected fingerprint is:

```text
F621 C843 74E5 2EF6 F0F9  B6FA A310 A531 2D2E E2C5
```

The X profile provides an identity channel independent of the release download. Compare the **entire fingerprint**, not a name, email address, or short key ID. The complete unspaced value is `F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5`.

On the offline machine, inspect the fingerprint of the downloaded key:

```sh
gpg --show-keys --fingerprint release-key.asc
```

Compare the complete fingerprint shown on the offline machine character for character with the independently published fingerprint on the other device. Stop if any character differs.

Import the key only after this comparison:

```sh
gpg --import release-key.asc
```

GPG may report that the key is “not certified with a trusted signature.” That message concerns the local web-of-trust calculation; it does not replace manual comparison of the full fingerprint.

## 4. Verify signature and archive on the offline machine

Keep the four transferred files in one otherwise empty directory on the permanently offline machine. All following verification output must come from this machine, not from the staging computer. First authenticate the checksum file:

```sh
gpg --verify SHA256SUMS.asc SHA256SUMS
```

The command must report a good signature made by the **complete expected fingerprint**. Treat warnings about an expired or revoked key, a different fingerprint, an invalid signature, or modified data as a failure. Do not continue based only on the words “Good signature”; confirm the signing-key fingerprint too.

Then verify the ZIP file against the now-authenticated checksum. Use the command for the offline machine's operating system.

Linux:

```sh
sha256sum --check SHA256SUMS
```

macOS:

```sh
shasum -a 256 --check SHA256SUMS
```

Windows PowerShell:

```powershell
$expected = (Get-Content .\SHA256SUMS).Split()[0]
$actual = (Get-FileHash .\RollYourOwnSeedphrase-offline-X.Y.Z-rcN.zip -Algorithm SHA256).Hash
$actual.ToLower() -eq $expected.ToLower()
```

Linux and macOS must report `OK`; Windows must report `True`. `SHA256SUMS` must name exactly the one versioned ZIP file. If either signature or checksum verification fails, stop and delete all four files. Never “fix” a checksum file or suppress an error.

Only after both checks succeed:

1. Use the offline machine's normal file manager to extract the verified ZIP into a new local folder.
2. Do not merge it into an older release.
3. Open only the extracted `index.html` as described below.

You may inspect or extract the ZIP on the staging computer, but do not trust or transfer that extracted copy. A compromised staging computer could change files after extraction. Transfer the original ZIP, verify it on the offline machine, and extract it there; this is normally only one additional file-manager action.

Advanced users should reproduce the release from the signed source tag on a separate verification system and compare the resulting archive byte-for-byte. That provides additional evidence, but the archive transferred to the seed machine must still pass the offline machine's own signature and checksum verification.

The offline checks are authoritative: the trusted GPG installation authenticates `SHA256SUMS`, and the offline operating system computes the ZIP's SHA-256 digest. A compromised staging computer cannot substitute another ZIP without either forging the release signature or presenting a different public key, which the independent full-fingerprint comparison is intended to detect.

## 5. Start the offline guide

1. On the permanently offline machine, open the verified release directory.
2. Open `index.html` directly in a locally installed browser. No web server, extension, installation, or network connection is required.
3. Confirm that the address begins with `file:` and that the browser shows no request to enable networking, install an extension, download a component, or grant unusual permissions.
4. Read and acknowledge Step 0. If every Step 0 condition is not true, close the guide without entering anything.
5. Follow the visual guide. In Step 3, select each die face in the fixed reading order; accepted results fill the bit rows and derive each BIP39 word automatically.
6. Verify every displayed bit group and word against your paper worksheet. After recording the result, click "Clear all" and confirm every bit and word disappears before leaving the page.

Do not use browser developer tools, translation, spell-check, synchronization, password-manager, accessibility-cloud, AI-assistant, or other extensions while handling seed material. The release is designed not to persist input, but the browser and operating system remain part of the trusted computing base.

## Updating the offline edition

Treat every update as a new package. Repeat acquisition, full-fingerprint confirmation, signature verification, checksum verification, and transfer from the beginning. Never overwrite files inside an older verified release or copy only changed JavaScript/HTML files. Keep versions in separate directories until the new release has been fully verified.

Release-key rotation must be announced and cross-signed by the previous valid key where possible, with both old and new full fingerprints published through independent channels. An unexplained key change is a reason to stop.

## What verification proves

Successful GPG and checksum verification establishes that the archive matches bytes signed by the holder of the expected release key. It does **not** prove that:

- the implementation is free of defects or malicious logic;
- the release or signing machine was uncompromised;
- the staging computer, removable media, offline machine, browser, or operating system is safe;
- the downloaded public key is authentic without independent fingerprint comparison; or
- the offline machine will remain safe if it is ever connected later.

Complete the [release procedure](RELEASING.md) and [verification checklist](TESTING.md) before relying on or releasing the offline edition.

Security reports must follow the repository's [private reporting policy](../SECURITY.md). Never include real seed material in a report.
