#!/usr/bin/env python3
"""Create and GPG-sign a release from a clean, reviewed source commit."""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "build-guides.py"
RELEASE_SIGNING_FINGERPRINT = "F621C84374E52EF6F0F9B6FAA310A5312D2EE2C5"
SPEC = importlib.util.spec_from_file_location("offline_build", BUILD_PATH)
assert SPEC and SPEC.loader
build_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_module)


def run(arguments: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, cwd=ROOT, check=True, capture_output=capture, text=True)


def require_clean_checkout() -> None:
    status = run(["git", "status", "--porcelain", "--untracked-files=all"], capture=True).stdout
    if status.strip():
        raise RuntimeError("Refusing to sign: the Git working tree is not clean.")


def require_version_tag(version: str) -> None:
    expected = f"v{version}"
    tags = run(["git", "tag", "--points-at", "HEAD"], capture=True).stdout.splitlines()
    if expected not in tags:
        raise RuntimeError(f"Refusing to sign: HEAD is not tagged {expected}.")


def require_secret_key(fingerprint: str) -> None:
    listing = run(
        ["gpg", "--batch", "--with-colons", "--fingerprint", "--list-secret-keys", fingerprint],
        capture=True,
    ).stdout
    fingerprints = [line.split(":")[9].upper() for line in listing.splitlines() if line.startswith("fpr:")]
    if fingerprint not in fingerprints:
        raise RuntimeError("The exact requested signing-key fingerprint is not available as a secret key.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version, for example 1.0.0")
    parser.add_argument("--signing-key", required=True, help="Complete 40-hex-character GPG fingerprint")
    args = parser.parse_args()
    fingerprint = args.signing_key.replace(" ", "").upper()
    if not re.fullmatch(r"[0-9A-F]{40}", fingerprint):
        parser.error("--signing-key must be the complete 40-hex-character fingerprint")
    if fingerprint != RELEASE_SIGNING_FINGERPRINT:
        parser.error("--signing-key does not match the published release-signing fingerprint")

    try:
        require_clean_checkout()
        require_version_tag(args.version)
        require_secret_key(fingerprint)
        archive = build_module.package(args.version)
        release = archive.parent
        signature = release / "SHA256SUMS.asc"
        public_key = release / "release-key.asc"
        signature.unlink(missing_ok=True)
        public_key.unlink(missing_ok=True)

        run([
            "gpg", "--batch", "--armor", "--detach-sign", "--local-user", fingerprint,
            "--output", str(signature), str(release / "SHA256SUMS")
        ])
        exported = run(["gpg", "--batch", "--armor", "--export", fingerprint], capture=True).stdout
        if "BEGIN PGP PUBLIC KEY BLOCK" not in exported:
            raise RuntimeError("GPG did not export the expected public release key.")
        public_key.write_text(exported, encoding="ascii", newline="\n")
        run(["gpg", "--batch", "--verify", str(signature), str(release / "SHA256SUMS")])
    except (RuntimeError, OSError, subprocess.CalledProcessError, build_module.BuildError) as error:
        print(f"release failed: {error}", file=sys.stderr)
        return 1

    print(f"signed release created in {archive.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
