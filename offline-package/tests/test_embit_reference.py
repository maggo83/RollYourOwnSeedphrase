from __future__ import annotations

import json
import random
import subprocess
import unittest
from collections.abc import Iterator
from pathlib import Path

try:
    from embit import bip39
except ModuleNotFoundError as error:
    raise RuntimeError(
        "Install pinned test dependencies with: "
        "python -m pip install --require-hashes -r offline-package/test-requirements.txt"
    ) from error

ROOT = Path(__file__).resolve().parents[2]
OFFLINE = ROOT / "dist" / "offline"
NODE_CHECKER = ROOT / "offline-package" / "tests" / "check_embit_vectors.js"
PSEUDORANDOM_CASES = 200_000


def generated_wordlist() -> list[str]:
    source = (OFFLINE / "bip39-english.js").read_text(encoding="utf-8")
    prefix = "globalThis.BIP39_ENGLISH_WORDS = Object.freeze("
    if not source.startswith("/* English BIP39 list") or prefix not in source or not source.rstrip().endswith(");"):
        raise AssertionError("The generated BIP39 word-list module has an unexpected format.")
    payload = source[source.index(prefix) + len(prefix):].rstrip()[:-2]
    return json.loads(payload)


def structured_entropy() -> Iterator[bytes]:
    for byte_length in (16, 32):
        for value in (0x00, 0xFF, 0x0F, 0xF0, 0x55, 0xAA):
            yield bytes([value]) * byte_length
        yield bytes(index & 0xFF for index in range(byte_length))
        yield bytes((255 - index) & 0xFF for index in range(byte_length))
        for bit in range(byte_length * 8):
            one_bit = bytearray(byte_length)
            one_bit[bit >> 3] = 1 << (7 - (bit & 7))
            yield bytes(one_bit)
            one_cleared_bit = bytearray([0xFF] * byte_length)
            one_cleared_bit[bit >> 3] &= ~(1 << (7 - (bit & 7)))
            yield bytes(one_cleared_bit)


def reference_vectors() -> Iterator[tuple[str, str, str]]:
    rng = random.Random(0xB1_39_EB_17)
    for entropy in structured_entropy():
        yield vector_from_entropy(entropy)
    for index in range(PSEUDORANDOM_CASES):
        yield vector_from_entropy(rng.randbytes(16 if index & 1 == 0 else 32))


def vector_from_entropy(entropy: bytes) -> tuple[str, str, str]:
    mnemonic = bip39.mnemonic_from_bytes(entropy)
    mnemonic_words = mnemonic.split()
    prefix_length = 7 if len(entropy) == 16 else 3
    entropy_bits = "".join(f"{byte:08b}" for byte in entropy)
    previous_bits = ",".join(
        entropy_bits[offset:offset + 11]
        for offset in range(0, (len(mnemonic_words) - 1) * 11, 11)
    )
    return entropy_bits[-prefix_length:], mnemonic_words[-1], previous_bits


class EmBitReferenceTests(unittest.TestCase):
    def test_generated_wordlist_matches_embit(self) -> None:
        self.assertEqual(generated_wordlist(), bip39.WORDLIST)

    def test_final_word_matches_embit(self) -> None:
        structured_count = sum(1 for _ in structured_entropy())
        expected_count = structured_count + PSEUDORANDOM_CASES
        process = subprocess.Popen(
            ["node", str(NODE_CHECKER), str(expected_count)],
            cwd=ROOT,
            stdin=subprocess.PIPE,
            text=True,
        )
        assert process.stdin is not None
        try:
            for prefix, expected, prior in reference_vectors():
                process.stdin.write(f"{prefix}\t{expected}\t{prior}\n")
        except BrokenPipeError:
            pass
        finally:
            process.stdin.close()
        self.assertEqual(process.wait(), 0, "Production bits-to-words code disagreed with EmBit reference vectors.")


if __name__ == "__main__":
    unittest.main()
