# Offline-edition verification

## Automated checks

Install the pinned test-only reference with `python -m pip install --require-hashes -r offline-package/test-requirements.txt`, then run `python offline-package/verify.py`. EmBit is used by Specter DIY and is never copied into a build or release. The suite verifies:

- deterministic online and offline assembly;
- exact ordered-fragment composition and generated online compatibility output;
- Step 0 and combined Step 3 variant isolation, including cross-contamination checks;
- local-only resources and forbidden browser capabilities;
- pinned BIP39 and SHA-256 source hashes;
- known SHA-256/BIP39 vectors plus direct comparison of the bundled SHA-256 against Node's implementation for structured edge patterns and 800,000 deterministic pseudorandom inputs;
- exact English-word-list equality and 200,784 final-word comparisons against EmBit 0.8.0, covering structured bit patterns and 200,000 deterministic pseudorandom 12-/24-word cases;
- invalid-input rejection; and
- byte-identical deterministic ZIP packaging.

## Browser review

Open `dist/offline/index.html` directly with a clean browser profile and no extensions.

1. Confirm Step 0 is first and blocks Continue until its acknowledgement is checked.
2. Complete the checklists with dummy data and confirm Steps 1–4 retain the online guide's layout and behavior.
3. In base-4 mode, confirm faces 1–4 append `00`, `01`, `10`, and `11`; faces 5–6 append nothing and show the skipped state.
4. Confirm Undo removes exactly the last accepted die result and Clear all empties every bit, word, checksum, progress value, and Step 3 checkpoint.
5. For 12 words, enter eleven rows of `00000000000` and final prefix `0000000`; the final checksum must be `0011` and the final word must be `about`.
6. Restart, choose 24 words, enter twenty-three rows of `00000000000` and final prefix `000`; the final checksum must be `01100110` and the final word must be `art`.
7. Type a non-binary character into a bit field and confirm it is removed without being echoed elsewhere.
8. Switch phrase length after entering dummy values and confirm all rows, results, progress, and completion state are cleared and rebuilt for the selected length.
9. Reload after entering dummy values; no entered values may return.
10. Inspect loaded resources: every resource must be a local `file:` URL within `dist/offline`, with no outbound or failed network request.
11. Confirm the console contains no seed data and browser storage, cookies, service workers, and cache storage remain empty.
12. Test desktop and narrow mobile layouts, Back/Continue navigation, keyboard digits 1–6, both encodings, and both rolling-container variants.

Use dummy vectors only during browser review. Never test with a real seed phrase on a connected development computer.
