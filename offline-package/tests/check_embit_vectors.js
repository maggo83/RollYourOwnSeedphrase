'use strict';

const fs = require('node:fs');
const path = require('node:path');
const readline = require('node:readline');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..', '..');
const offline = path.join(root, 'dist', 'offline');
for (const file of ['bip39-english.js', 'sha256.js', 'bits-words.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(offline, file), 'utf8'), { filename: file });
}

const expectedCount = Number.parseInt(process.argv[2], 10);
if (!Number.isSafeInteger(expectedCount) || expectedCount < 1) throw new Error('Expected a positive vector count.');

const words = globalThis.BIP39_ENGLISH_WORDS;
const derive = globalThis.OfflineBitsWordsCore.deriveFinalWord;
const sha256 = globalThis.OfflineHash.sha256;
let checked = 0;

const lines = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
lines.on('line', line => {
  const firstTab = line.indexOf('\t');
  const secondTab = line.indexOf('\t', firstTab + 1);
  if (firstTab < 1 || secondTab < firstTab + 2) throw new Error(`Malformed reference vector ${checked}.`);
  const prefix = line.slice(0, firstTab);
  const expected = line.slice(firstTab + 1, secondTab);
  const previousBits = line.slice(secondTab + 1).split(',');
  const mnemonicLength = prefix.length === 7 ? 12 : prefix.length === 3 ? 24 : 0;
  const actual = derive(previousBits, prefix, mnemonicLength, words, sha256).word;
  if (actual !== expected) throw new Error(`EmBit reference mismatch at vector ${checked}: ${actual} != ${expected}`);
  checked += 1;
});
lines.on('close', () => {
  if (checked !== expectedCount) throw new Error(`Checked ${checked} EmBit vectors; expected ${expectedCount}.`);
  console.log(`EmBit final-word reference comparisons passed: ${checked}`);
});
